# CodeWarrior Companion Lane

This directory is the `companion` compatibility-technology lane for `metrowerks.codewarrior`. It is an AIDE fallback for archival or unresolved CodeWarrior workflows that do not map cleanly onto the documented native SDK lane.

P13 adds a runnable companion boot-slice proof through `cli-bridge` mode:

- `run_boot_slice.py` is a thin lane-local shim that invokes `shared.cli`
- `boot_slice_request.json` records the committed lane-shaped request
- `boot_slice_response.json` records the expected deterministic response

This proof intentionally stops at `L1` fallback invocation. It does not replace the archival-native `ide-sdk` lane; it keeps unresolved or non-native CodeWarrior workflows moving while native historical environments and deeper editor proofs remain deferred. Exact version coverage is tracked in inventory and matrices.
