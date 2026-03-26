# CodeWarrior IDE SDK Lane

This directory is the `ide-sdk` compatibility-technology lane for `metrowerks.codewarrior`. In current research it is exact for preserved classic CodeWarrior SDK and COM automation manuals, and only an AIDE umbrella for later Eclipse-based CodeWarrior families.

P13 adds a runnable archival-native boot-slice proof through `cli-bridge` mode:

- `run_boot_slice.py` is a thin lane-local shim that invokes `shared.cli`
- `boot_slice_request.json` records the committed lane-shaped request
- `boot_slice_response.json` records the expected deterministic response
- `plugin-target.yaml` keeps the native SDK or COM entry surface visible without pretending native loading was verified here

This proof intentionally stops at `L1` report-first invocation. Native CodeWarrior IDE SDK loading, COM automation wiring, and optional editor-marker proof remain blocked or deferred by missing historical environments and unresolved classic-versus-later contract boundaries. Exact version coverage is tracked in inventory and matrices.
