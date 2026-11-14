# Evidence v1 for Before Model Escalation

This evidence release accompanies manuscript revision v11, submitted to arXiv on November 14, 2026. Public announcement and a public identifier are pending. Original code is MIT licensed; original data/documentation and the manuscript are CC BY 4.0. Third-party terms and exceptions are documented in LICENSE-SCOPE.md.

The release contains 8 frozen evidence archives, the paper PDF and its source. All 10 asset hashes match the inspected manuscript release. Original scientific records, including negative results and failed runtime attempts, are unchanged. The allowance archive's historical internal manifest omits its README; `artifacts.json` explicitly supplies that file's checksum in addition to the complete frozen archive hash.

The public entry point verifies every archive manifest and recounts the primary recorded evidence with Python's standard library. It does not rerun hosted models or browser actions. The original strict runtime replays remain failed. The separate adjusted-deadline study and its limitations are reported as such.

The application subset omits product-bearing source, HTML, media and screenshots and retains their hashes; it recomputes recorded summaries, not the complete application audit. The diagnostic pilot runs are outside this release.

No DOI or public arXiv identifier is assigned here. Citation metadata will be updated with actual identifiers when available. Read README.md, reuse/README.md, THIRD_PARTY_NOTICES.md and the licensing scope before reuse.

The repository includes a data dictionary, tested recount example, full original-code/data license texts and retained third-party notices. Download assets with `python3 download_assets.py --assets assets`; verify with `python3 verify_release.py --assets assets`.
