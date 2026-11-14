# Reading the primary records

This guide describes the frozen instruction controls and deadline comparison in manuscript v11. It documents existing records; it does not introduce new outcomes, recode failures or validate task definitions. Verify the asset hashes before analysis. The archived source is authoritative when a shorter description here is insufficient.

## Model comparisons: files and observation units

Inside `instruction-control-evidence.zip`, the main run is `instruction-control-evidence/replication/mistral-control-main-01/`. Inside `qwen-instruction-control-evidence.zip`, it is `qwen-instruction-control-evidence/replication/qwen-control-main-01/`.

| File | Contents |
| --- | --- |
| `config.json` | Requested model/provider configuration, task types, seeds and the 4 schema/instruction conditions |
| `jobs.json` | Scheduled jobs; completed journal order can differ because workers run concurrently |
| `episodes.jsonl` | 540 completed records per main run: 240 trajectories and 300 one-action probes |
| `calls.jsonl` | Request and response events, paired by `callId`; 1,872 events for 936 Ministral calls and 1,944 events for 972 Qwen calls |
| `analysis.json`, `summary.csv` | Original derived summaries, including failure and cost categories |
| `pages/`, `manifest.json`, `source/` | Recorded page artifacts, provenance and the exact implementation used by that run |

Each JSONL line is an envelope with `sequence`, `previousHash`, `data` and `recordHash`. The observation is in `data`. These are hash-chained journals: sorting lines or rewriting JSON changes their integrity representation. The archived `source/src/journal.ts` and `source/src/util.ts` define the original check; a simple row-reading example is not a replacement for it.

Each model run has 4 conditions. A condition has 60 trajectories: 12 known task types with 5 generated seeds each. It also has 75 probes: 60 initial-state probes and 15 pre-submit probes on applicable tasks. The two modes have different denominators. Repeated conditions, seeds, task types and constructed states are dependent; 540 records are not 540 independent tasks.

| Episode field (`data.*`) | Meaning and interpretation |
| --- | --- |
| `id` | Identifier for this condition-specific record, also used by the call journal's `episodeId` |
| `task`, `seed` | MiniWoB task type and generated instance seed; neither identifies a new application |
| `conditionId` | `<model>-<legacy or conditional>-<original or explicit>`; the exact definition is in `config.json` |
| `mode`, `state` | `trajectory` or `probe`; `initial` or `pre-submit` |
| `fullCredit` | Main completion outcome. The archived scorer requires no episode-level error, a terminal validator state, and `validation.info.RAW_REWARD_GLOBAL >= 1` |
| `success` | Positive-reward outcome. The scorer requires no episode-level error, a terminal state, and `validation.reward > 0`; it is not interchangeable with full credit |
| `validation` | Native reward, terminal flag, message and underlying task fields |
| `stop` | Runner stop label such as `benchmark-terminated`, `probe-complete`, `step-limit` or `invalid-output`; it is not a mutually exclusive causal failure diagnosis |
| `error`, `artifactError` | Episode-level and artifact-capture errors, respectively; separate from individual attempt/tool errors |
| `attempts[]` | Observation, history, request seed and model result for each attempted model call |
| `steps[]` | Tool/result records with before/after validators, `executed` and `executionError`; a successful tool return alone is not task completion |
| `artifacts` | Recorded file paths mapped to hashes |
| `durationMs` | Episode duration in milliseconds; includes work beyond model inference |

Pair conditions within a run by `(mode, task, seed, state)`. `id` differs across conditions and is not the pairing key. Restrict to `mode == "trajectory"` for the main full-credit comparison. Keep every attempted trajectory, including transport failures, in its condition's denominator. The two models were run separately with different serving packages; joining their rows does not create a randomized model-family or capacity comparison.

## Failure categories and costs

`attempts[].result` retains the parsed `action`, raw reply, `error`, `request`, `requestHash`, `callId`, `transport`, `usage`, `providerUsage`, returned model and finish reason. The call journal duplicates request/response information for auditing; do not count both a request event and its response as 2 model calls.

The archived `source/src/replication/audit.ts::classify` distinguishes provider failures, malformed JSON, invalid actions, unavailable references and requested-schema validity. Its provider-failure predicate uses the recorded error string. HTTP status and error-body evidence are retained in `transport`. A `stop` value of `invalid-output` does **not** by itself mean the model generated malformed JSON: all 3 failed Qwen trajectories have that runner label, while their terminal attempts contain 2 HTTP 502 failures and 1 request timeout. They remain failed trajectories.

`usage.costUsd` is denominated in USD and can be null. `usage.costSource == "provider"` identifies confirmed costs in the original summary; other costs remain unresolved rather than becoming free. `reservedUsd` on request events is a conservative budget reservation, not an invoice. `usage.latencyMs` is call latency in milliseconds. The paper's main cost cells concern trajectory calls, while the complete run's call count also includes probes. Use the archived analysis for exact accounting and retain failed calls.

## Small full-credit recount

After the documented verification command passes, run this Python example from the release repository with the downloaded ZIPs in `assets/`. It reads the original ZIP members without extracting or modifying them. It prints the 8 condition totals and explicit-instruction discordant counts. It does not validate journal chains, rescore native tasks or classify costs.

```python
import collections
import json
import pathlib
import zipfile

asset_dir = pathlib.Path("assets")
for model, filename in [
    ("mistral", "instruction-control-evidence.zip"),
    ("qwen", "qwen-instruction-control-evidence.zip"),
]:
    prefix = filename.removesuffix(".zip")
    member = f"{prefix}/replication/{model}-control-main-01/episodes.jsonl"
    with zipfile.ZipFile(asset_dir / filename) as archive:
        records = [json.loads(line)["data"] for line in archive.read(member).splitlines()]
    groups = collections.defaultdict(dict)
    for row in records:
        if row["mode"] != "trajectory":
            continue
        key = (row["task"], row["seed"], row["state"])
        group = groups[row["conditionId"]]
        assert key not in group and type(row["fullCredit"]) is bool
        group[key] = row["fullCredit"]
    for condition, group in sorted(groups.items()):
        assert len(group) == 60
        print(condition, sum(group.values()), len(group))
    legacy = groups[f"{model}-legacy-explicit"]
    conditional = groups[f"{model}-conditional-explicit"]
    assert legacy.keys() == conditional.keys()
    print(model, "legacy-only", sum(legacy[k] and not conditional[k] for k in legacy),
          "conditional-only", sum(conditional[k] and not legacy[k] for k in legacy))
```

Expected explicit-instruction results: Ministral 51/60 in each arm, 3 successes unique to each; Qwen 58/60 versus 59/60, with 1 legacy-only and 2 conditional-only successes. These discordances do not establish equivalence or a semantic benefit from the Qwen gap.

## Deadline comparison: returned status and observed effects

In `browser-runtime-repair-evidence.zip`, the two data files are `results/browser-runtime-repair-main-01/results.json` and `results/browser-runtime-repair-fresh-01/observations/results.json`, beneath the archive's top-level directory. Each has 138 entries in `results`: 23 fixed cases × 3 blocks × 2 deadlines. Each case-arm run supplies 2 tool-call responses. Across environments that is 276 case-arm runs and 552 supplied `get_action` calls, with **0 model inference calls**.

| Field | Meaning |
| --- | --- |
| Top-level `stage` | `main` or `fresh`; the fresh environment remains on the same host |
| `results[].id`, `block`, `timeoutMs` | Fixed case, repetition block (0–2), and explicit deadline arm (500 or 5,000 ms) |
| `operation`, `arguments` | Fixed first action and supplied arguments; the second action fills the designated field with `verified` |
| `steps[].schemaAccepted`, `parserAccepted`, `parsedArgumentTypes` | Separate interface checks; none alone establishes execution or task success |
| `steps[].executed`, `error` | Returned execution status/error; a timeout remains a failed return even when a page effect is visible |
| `steps[].state`, `activeInputValue` | Observed page state and field content, inspected separately from returned status |
| `firstPriorControlAgreement` | Agreement with the original first-control action/acceptance/returned-status/state fields; expected rejection controls count as matches |
| `secondFillExecuted` | A successful second return **and** field value `verified` |
| `priorToolResponseIncluded`, `actualErrorIncluded` | Checks that the supplied second call saw the recorded preceding response/error |
| `trace`, `traceSha256` | Relative trace path and hash |
| `steps[].deadlineEdits`, `originalCodeSha256`, `executedCodeSha256` | Evidence of the explicit generated-code deadline intervention |

Pair environments by `(block, id, timeoutMs)` and compare the same step. Pair deadline arms within an environment by `(block, id)`. The cross-environment comparison uses a specified list of outcome/message fields in `reports/analyze-runtime-repair.py`, not byte equality of trace files or timing measurements. The archive contains 276 traces. The 69 observations per arm/environment repeat 23 known cases; they are not 69 independent tasks.

The intervention alters literal `timeout=500` keywords in generated action code to 5,000 ms and retains the installed upstream source. It is an adjusted executor, not a successful unchanged-upstream replay. Substantial shared-machine load, the old Python Playwright/new Chromium combination, and the fresh environment's source-copy versus later archive-extraction distinction remain disclosed in its README and protocol.

## Locating the paper's tables

The manuscript source ZIP contains `generated/instruction-control.tex`, `generated/qwen-instruction-control.tex` and `generated/runtime-repair-table.tex`. The first two distinguish the 75-probe rejection denominator from the 60-trajectory full-credit/cost denominator. The last uses 69 case runs per arm/environment and retains expected argument-error controls. Read each caption and the corresponding archived protocol before pooling or reusing observations.
