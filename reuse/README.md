# Reuse the comparisons and software cases

Companion to **Before Model Escalation: Contracts, Instructions, and Outcomes in Browser Agents**, manuscript v11, by Tejas Kumar. [Versioned evidence and paper](https://github.com/TejasQ/before-model-escalation/releases/tag/evidence-v1). The paper has been submitted to arXiv; its public identifier and announcement are pending. No DOI or independent scientific replication is claimed. Original code is MIT licensed; original data/documentation and the manuscript are CC BY 4.0. Third-party terms remain in force. See [the license scope](../LICENSE-SCOPE.md).

## Start with a recorded-evidence check

From the project root, using only Python 3's standard library:

```sh
python3 reuse/verify.py --archives assets
```

Download the 4 selected evidence ZIPs into `assets/` using `python3 download_assets.py --assets assets --primary`, or download all 10 assets for the complete release check. No dependency installation, model key, inference, browser, signed-in profile, or network access is needed. It verifies the 4 frozen archives and every member hash, recounts all 480 main trajectories from the original 1,080 mixed records, checks the 2 explicit-instruction paired comparisons, runs the original recorded-data agent-loop checker against its supplied records and upstream wheels, and verifies the complete new deadline-intervention records and 276 trace archives. Add `--receipt /new/path.json` to save the result without overwriting an old receipt.

**This check verifies retained evidence without rerunning hosted models or a browser.** It does not regenerate every paper table or validate scientific task definitions. The original unmodified browser-runtime criterion remains failed, recorded as `originalUnmodifiedRuntimeReplayPassed: false`. The separate 5-second deadline intervention passed its actual runtime comparisons in both environments; this command independently recounts those saved records. A zero exit status means the stated recorded-evidence checks passed.

## Choose the evidence your research needs

| Research question | Reusable material | What it supports | What it does not support |
| --- | --- | --- | --- |
| Does a schema intervention help beyond explicitly stating runtime rules? | `instruction-control-evidence.zip`, `replication/mistral-control-main-01/`: frozen protocol, conditions, task seeds, original source, requests/replies, journals and native outcome records | A fixed 4-condition comparison: original instructions 45/60 vs 49/60; explicit instructions 51/60 each, with 3 unique successes each | Equivalence, a general schema effect, or a transferable router |
| Does that comparison behave the same under another serving package? | `qwen-instruction-control-evidence.zip`, `replication/qwen-control-main-01/` | Separately scheduled Qwen 27B control: original 60/60 each; explicit 58/60 vs 59/60, retaining transport failures | An isolated capacity/family effect, or evidence of a semantic gain from the 1-case gap |
| Can schema acceptance, argument acceptance, returned status and observed effects disagree? | `released-agent-loop-evidence.zip`, `reviews/released-agent-loop-01/`: all 23 software cases, supplied SDK responses, frozen harness, wheel provenance and raw diagnostic replay | Fixed counterexamples and traces; a timeout may follow a click or field change | A natural failure rate, successful retry policy, full native benchmark reproduction, or model-generated correction ability |
| Does a longer explicit deadline remove the observed execution mismatches? | `browser-runtime-repair-evidence.zip`: all 23 controls, 3 paired blocks per environment, frozen source and 276 traces | Original 500 ms arms: 13 timeouts, 11 with effects; adjusted 5-second arms: zero timeouts, all controls/fills matched, 69/69 paired outcome/message records agree across environments | A natural failure rate, independent tasks, an optimal deadline, unchanged-upstream replay or production reliability |

The 2 model controls use known MiniWoB task types with 60 instances per condition. Probes and repeated conditions are dependent. The 23 software cases are selected counterexamples and controls. Treat the released artifacts as scoped comparisons and regression inputs, not a representative benchmark leaderboard.

## Recompute original analyses or inspect the runtime

Extract an evidence ZIP and read its own `README.md` before running its commands. These retain the archived source and original definitions rather than substituting the new lightweight recount.

| Extracted archive root | Command | Dependencies and scope |
| --- | --- | --- |
| `instruction-control-evidence/` | `python3 reports/reproduce-mistral-control.py` | Python 3, Node 22.12+, npm; fresh locked installs may download dependencies; exact-source saved-data analyses, no browser/inference |
| `qwen-instruction-control-evidence/` | `python3 reports/reproduce-qwen-control.py` | Same requirements; exact-source saved-data analyses, no browser/inference |
| `released-agent-loop-evidence/` | `python3 reports/verify-agent-loop-records.py` | Python standard library; posthoc checks of supplied records and wheel members |
| `released-agent-loop-evidence/` | `python3.11 reports/reproduce-agent-loop.py` | Python 3.11, pinned minimal runtime, Node/npm, bundled Chromium, package downloads; actual software runtime replay; strict comparison can fail and 2 retained runs did fail |
| `browser-runtime-repair-evidence/` | `python3 reports/analyze-runtime-repair.py --main results/browser-runtime-repair-main-01 --fresh results/browser-runtime-repair-fresh-01/observations --out recount.json` | Python standard library; saved-record recount and trace/source verification, no browser |
| `browser-runtime-repair-evidence/` | `python3 reports/reproduce-runtime-repair.py --work /absolute/path/to/new-runtime-check` | Python 3.11, Node/npm, pinned browser and package downloads; new actual browser grid, all outputs retained, no inference |

Read `reviews/browser-runtime-repair-01/README.md` inside the new archive for the intervention, shared-machine load, source-copy versus archive-extraction distinction and limits. New runtime results may differ.

The complete project also provides separate exporter, consumer-boundary, allowance and earlier-study archives, indexed in `artifacts.json`. All 8 evidence archives are available as release assets; the focused command above checks 4 of them. In the earlier app subset, product-bearing source/page/media files are omitted and their hashes inventoried; it cannot reproduce a full app-artifact audit. This kit does not silently stand in for those materials or for every project record.

## Cite the specific contribution you used

`CITATION.cff` supplies machine-readable metadata and a preferred citation to the manuscript. `citation.bib` is an unpublished-draft BibTeX entry. Both use the manuscript's current author line and title. They identify the public evidence repository and omit an arXiv identifier or DOI until those exist. The public artifact version has a GitHub release URL. The actual arXiv identifier will be added after announcement; none is invented here. Independent human scientific review has not been received.

A paper comparing schemas with language instructions can cite the paired control. A software-validation paper can cite the fixed conformance cases. An agent-execution paper can cite the distinction between returned status and observed effects. Report the scope and denominators of the evidence you use. A citation is warranted by use of the work, not required as a condition of reproducing its claims.
