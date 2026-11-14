#!/usr/bin/env python3
"""Download versioned public evidence, verifying every asset before keeping it."""
import argparse
import hashlib
import json
import pathlib
import urllib.request

BASE = pathlib.Path(__file__).resolve().parent
URL = "https://github.com/TejasQ/before-model-escalation/releases/download/evidence-v1/"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--assets', type=pathlib.Path, default=BASE / 'assets')
    parser.add_argument('--primary', action='store_true', help='Only the 4 archives used by reuse/verify.py')
    args = parser.parse_args()
    expected = json.loads((BASE / 'artifacts.json').read_text())
    if args.primary:
        selected = json.loads((BASE / 'reuse/expected-artifacts.json').read_text())
        expected = {name: expected[name] for name in selected}
    args.assets.mkdir(parents=True, exist_ok=True)
    for name, entry in expected.items():
        path = args.assets / name
        if path.exists():
            if path.stat().st_size != entry['bytes'] or hashlib.sha256(path.read_bytes()).hexdigest() != entry['sha256']:
                raise ValueError('Existing file differs; preserve it and choose a new directory: ' + str(path))
            print('Verified existing', name)
            continue
        temporary = path.with_name(path.name + '.part')
        digest = hashlib.sha256()
        size = 0
        with temporary.open('xb') as output:
            try:
                request = urllib.request.Request(URL + name, headers={'User-Agent': 'before-model-escalation-evidence/1'})
                with urllib.request.urlopen(request, timeout=120) as response:
                    while chunk := response.read(1024 * 1024):
                        output.write(chunk)
                        digest.update(chunk)
                        size += len(chunk)
                if size != entry['bytes'] or digest.hexdigest() != entry['sha256']:
                    raise ValueError('Downloaded asset mismatch: ' + name)
            except BaseException:
                temporary.unlink(missing_ok=True)
                raise
        temporary.rename(path)
        print('Downloaded and verified', name)


if __name__ == '__main__':
    main()
