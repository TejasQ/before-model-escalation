# Before Model Escalation

Evidence for **Before Model Escalation: Contracts, Instructions, and Outcomes in Browser Agents**, by Tejas Kumar.

**Current manuscript: v12.** [Read the paper](https://github.com/TejasQ/before-model-escalation/releases/download/manuscript-v12/browser-agent-evaluation.pdf) or [download its source](https://github.com/TejasQ/before-model-escalation/releases/download/manuscript-v12/browser-agent-paper-source.zip). [Evidence release v1](https://github.com/TejasQ/before-model-escalation/releases/tag/evidence-v1) remains the fixed experimental archive. The manuscript was submitted to arXiv on November 14, 2026; public announcement and an arXiv identifier are pending. Original code is MIT licensed. Original data, documentation and the paper are CC BY 4.0. [License scope and third-party exceptions](LICENSE-SCOPE.md).

## What this work contributes

Browser-agent failures can occur before reasoning is the limiting factor. This study compares action schemas with explicit runtime instructions and examines disagreement between returned action status and observed page effects.

- In the fixed Ministral 14B control, original instructions yield 45/60 versus 49/60 successful trajectories with legacy versus conditional schemas. Explicit runtime instructions yield 51/60 in each arm, with 3 unique successes in each. Equal totals do not establish equivalence.
- In the separately scheduled Qwen 27B control, original instructions yield 60/60 in both arms. Explicit instructions yield 58/60 versus 59/60; all 3 failures stop at transport errors. The comparison does not isolate model family or capacity.
- In selected released-software cases, schema acceptance, argument acceptance, returned status and observed effects can differ. Two original fresh browser replays failed their strict comparison.
- A separate intervention changes explicit BrowserGym deadlines from 500 to 5,000 ms. Across 2 environments, the original arms show 13 timeouts, 11 with observed effects; adjusted arms show none. All 69 paired adjusted outcome/message records agree across environments. These are 23 known cases repeated in 3 blocks, not independent tasks or a production reliability estimate.

The paper retains failed controller transfer, negative history results and failed runtime attempts. It does not establish a validated router, an optimal deadline, a natural failure rate, or independent peer review.

## Read and verify

Evidence-v1 contains the earlier v11 manuscript PDF/source and 8 frozen evidence ZIPs. Manuscript-v12 changes only 4 appendix availability/license passages, linking the public evidence. All scientific results, tables, figure and references are unchanged; its 2 file hashes are in `manuscript-v12.json`. The commands below deliberately verify the immutable evidence-v1 snapshot. Download the files with hash verification, then check the retained evidence:

```sh
python3 download_assets.py --assets assets
python3 verify_release.py --assets assets
```

Python 3's standard library is sufficient. This verifies all asset hashes and all manifest-listed ZIP members, then runs the focused recorded-evidence check. The download command fetches the versioned GitHub assets and verifies their hashes. The verification command makes no network requests, calls no model and launches no browser. A pass verifies retained records; it is not a live replication of model behavior or an independent validation of task definitions.

For the smaller primary check, download the 4 archives named in `reuse/expected-artifacts.json` and run `python3 reuse/verify.py --archives assets`. See `reuse/README.md` for per-study analysis and browser replay commands. [The data dictionary](reuse/DATA_DICTIONARY.md) explains record fields, pairing keys, denominators and failure/cost categories, with an executable full-credit recount example.

| Asset | Contents and limits |
| --- | --- |
| [browser-agent-evaluation.pdf](https://github.com/TejasQ/before-model-escalation/releases/download/evidence-v1/browser-agent-evaluation.pdf) | Earlier v11 manuscript snapshot; current v12 linked above |
| [browser-agent-paper-source.zip](https://github.com/TejasQ/before-model-escalation/releases/download/evidence-v1/browser-agent-paper-source.zip) | TeX source, figure, tables and derivations |
| [instruction-control-evidence.zip](https://github.com/TejasQ/before-model-escalation/releases/download/evidence-v1/instruction-control-evidence.zip) | Ministral paired schema/instruction control, including smoke records |
| [qwen-instruction-control-evidence.zip](https://github.com/TejasQ/before-model-escalation/releases/download/evidence-v1/qwen-instruction-control-evidence.zip) | Separately scheduled Qwen control; transport failures retained |
| [released-interface-conformance-evidence.zip](https://github.com/TejasQ/before-model-escalation/releases/download/evidence-v1/released-interface-conformance-evidence.zip) | Fixed released-interface conformance cases |
| [released-consumer-boundary-evidence.zip](https://github.com/TejasQ/before-model-escalation/releases/download/evidence-v1/released-consumer-boundary-evidence.zip) | Released exporter/consumer boundary cases |
| [released-agent-loop-evidence.zip](https://github.com/TejasQ/before-model-escalation/releases/download/evidence-v1/released-agent-loop-evidence.zip) | Supplied-response agent integration and original failed browser comparisons |
| [browser-runtime-repair-evidence.zip](https://github.com/TejasQ/before-model-escalation/releases/download/evidence-v1/browser-runtime-repair-evidence.zip) | Paired 500/5,000 ms intervention, 276 case-arm runs and 276 trace archives |
| [allowance-sensitivity-evidence.zip](https://github.com/TejasQ/before-model-escalation/releases/download/evidence-v1/allowance-sensitivity-evidence.zip) | Two interrupted allowance studies; no complete effect estimate |
| [earlier-study-evidence.zip](https://github.com/TejasQ/before-model-escalation/releases/download/evidence-v1/earlier-study-evidence.zip) | Five earlier MiniWoB study archives and an app-summary subset; product-bearing app source and media omitted, with hashes retained |

Archives are immutable historical evidence. Their internal publication-status statements describe the time they were packaged; the dated outer release record governs current availability. No experimental file has been edited for this release. The earlier-study archive does not include the diagnostic pilot runs or provide a full application-artifact audit.

## Citation and critical review

Use `CITATION.cff` or `citation.bib` for the actual contribution you use. Neither invents an arXiv identifier or DOI. The identifier will be added after announcement. Citation is requested for scholarly attribution, not imposed as a condition of checking the findings.

To report a problem, include the archive hash, exact command, environment, observed result and expected result. Read `REVIEW.md` for the main scientific questions. Automated and author-directed checks are disclosed; independent human scientific review has not been received.

## Rights and provenance

Original code is licensed under [MIT](LICENSE); original data, documentation and the paper are [CC BY 4.0](LICENSES/CC-BY-4.0.txt). [LICENSE-SCOPE.md](LICENSE-SCOPE.md) defines the grants and exclusions. Third-party materials retain their own notices and licenses; `THIRD_PARTY_NOTICES.md` and `third_party/notices.json` locate the retained notice texts.
