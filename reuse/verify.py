#!/usr/bin/env python3
"""Verify frozen evidence and recount primary outcomes, without inference or a browser."""
import argparse
import collections
import hashlib
import json
import pathlib
import subprocess
import sys
import tempfile
import zipfile

BASE = pathlib.Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def verify_archive(path, destination):
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)), 'Duplicate ZIP member')
        manifests = [n for n in names if n.count('/') == 1 and n.endswith('/SHA256SUMS.json')]
        require(len(manifests) == 1, 'Expected one root checksum manifest')
        manifest_name = manifests[0]
        prefix = manifest_name.rsplit('/', 1)[0] + '/'
        sums = json.loads(archive.read(manifest_name))
        require(set(names) == {prefix + n for n in sums} | {manifest_name}, 'Unlisted ZIP member')
        for name in names:
            p = pathlib.PurePosixPath(name)
            require(not p.is_absolute() and '..' not in p.parts and '\\' not in name,
                    'Unsafe archive path')
            require(not ((archive.getinfo(name).external_attr >> 16) & 0o170000 == 0o120000),
                    'ZIP symlinks are not supported')
        for name, expected in sums.items():
            require(hashlib.sha256(archive.read(prefix + name)).hexdigest() == expected,
                    'Member hash mismatch: ' + name)
        archive.extractall(destination)
    return destination / prefix.rstrip('/'), len(sums)


def recount(root, model):
    path = root / 'replication' / (model + '-control-main-01') / 'episodes.jsonl'
    records = [json.loads(line)['data'] for line in path.read_text().splitlines()]
    require(len(records) == 540, 'Expected 540 mixed records')
    modes = collections.Counter(r['mode'] for r in records)
    require(modes == {'probe': 300, 'trajectory': 240}, 'Unexpected record modes')
    groups = collections.defaultdict(dict)
    for record in records:
        if record['mode'] == 'trajectory':
            key = (record['task'], record['seed'])
            group = groups[record['conditionId']]
            require(key not in group, 'Duplicate task/seed within condition')
            require(type(record['fullCredit']) is bool, 'Expected Boolean fullCredit')
            group[key] = record['fullCredit']
    expected = {'mistral': [45, 49, 51, 51], 'qwen': [60, 60, 58, 59]}[model]
    labels = ['legacy-original', 'conditional-original', 'legacy-explicit', 'conditional-explicit']
    totals = {}
    for label, count in zip(labels, expected):
        group = groups[model + '-' + label]
        require(len(group) == 60 and sum(group.values()) == count, 'Primary total differs: ' + label)
        totals[label] = {'fullCredit': count, 'attempted': len(group)}
    a = groups[model + '-legacy-explicit']
    b = groups[model + '-conditional-explicit']
    require(a.keys() == b.keys(), 'Unpaired explicit-instruction instances')
    paired = dict(collections.Counter(
        'both' if a[k] and b[k] else 'legacyOnly' if a[k] else 'conditionalOnly' if b[k] else 'neither'
        for k in a))
    expected_pairs = {'mistral': {'both': 48, 'legacyOnly': 3, 'conditionalOnly': 3, 'neither': 6},
                      'qwen': {'both': 57, 'legacyOnly': 1, 'conditionalOnly': 2}}[model]
    require(paired == expected_pairs, 'Paired discordances differ')
    return {'mixedRecords': len(records), 'totals': totals, 'explicitPairs': paired}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archives', type=pathlib.Path, default=BASE.parent / 'output')
    parser.add_argument('--receipt', type=pathlib.Path,
                        help='Optional new receipt path; existing files are never overwritten')
    args = parser.parse_args()
    if args.receipt and args.receipt.exists():
        parser.error('Receipt already exists; choose a new path')
    frozen = json.loads((BASE / 'expected-artifacts.json').read_text())
    receipt = {'scope': __doc__, 'archives': {}, 'primaryComparisons': {},
               'additionalModelCalls': 0, 'runtimeReplayPerformed': False,
               'originalUnmodifiedRuntimeReplayPassed': False, 'independentScientificReplication': False}
    with tempfile.TemporaryDirectory(prefix='browser-agent-recorded-evidence-') as directory:
        temp = pathlib.Path(directory)
        for filename, specification in frozen.items():
            path = args.archives / filename
            require(path.is_file(), 'Missing artifact: ' + filename)
            require(path.stat().st_size == specification['bytes'], 'Artifact size differs: ' + filename)
            require(digest(path) == specification['sha256'], 'Artifact hash differs: ' + filename)
            root, count = verify_archive(path, temp)
            receipt['archives'][filename] = {'sha256': specification['sha256'], 'memberHashesVerified': count}
            if filename == 'released-agent-loop-evidence.zip':
                run = subprocess.run([sys.executable, 'reports/verify-agent-loop-records.py'],
                                     cwd=root, text=True, capture_output=True)
                require(run.returncode == 0, 'Recorded agent-loop check failed: ' + run.stderr[-1500:])
                receipt['recordedAgentLoop'] = json.loads(
                    (root / 'reports/agent-loop-recorded-verification.json').read_text())
                require(receipt['recordedAgentLoop']['fullRuntimeReplayPassed'] is False,
                        'Failed runtime evidence was changed')
            elif filename == 'browser-runtime-repair-evidence.zip':
                run = subprocess.run([sys.executable, 'reports/analyze-runtime-repair.py',
                    '--main', 'results/browser-runtime-repair-main-01',
                    '--fresh', 'results/browser-runtime-repair-fresh-01/observations',
                    '--out', 'recount.json'], cwd=root, text=True, capture_output=True)
                require(run.returncode == 0, 'Recorded deadline comparison failed: ' + run.stderr[-1500:])
                actual = json.loads((root / 'recount.json').read_text())
                expected = json.loads((root / 'reports/browser-runtime-repair-analysis.json').read_text())
                actual.pop('checkedAt'); expected.pop('checkedAt')
                require(actual == expected, 'Recorded deadline comparison changed')
                receipt['recordedDeadlineRepair'] = actual
            else:
                model = 'qwen' if filename.startswith('qwen-') else 'mistral'
                receipt['primaryComparisons'][model] = recount(root, model)
    text = json.dumps(receipt, indent=2) + '\n'
    if args.receipt:
        with args.receipt.open('x') as stream:
            stream.write(text)
    print(text, end='')


if __name__ == '__main__':
    main()
