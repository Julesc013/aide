# Visual Studio COM Add-in Lane

This directory is the `com-addin` compatibility-technology lane for `microsoft.visual-studio`. In this repository it remains a conservative umbrella for pre-VSIX legacy native Visual Studio extensibility rather than a full historical taxonomy.

P11 adds a degraded but runnable boot-slice proof through `cli-bridge` mode:

- `run_boot_slice.py` is a thin lane-local shim that invokes `shared.cli`
- `boot_slice_request.json` records the committed lane-shaped request
- `boot_slice_response.json` records the expected deterministic response

This proof is intentionally report-first and stops at `L1`. Native COM add-in loading, host detection, and editor wiring remain blocked by the missing legacy Visual Studio environment and unresolved pre-2010 contract detail.
