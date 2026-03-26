# Visual Studio VSIX v1 Lane

This directory is the `vsix-v1` compatibility-technology lane for `microsoft.visual-studio`. It represents the initial Visual Studio 2010-era VSIX packaging family.

P11 adds a degraded but runnable boot-slice proof through `cli-bridge` mode:

- `run_boot_slice.py` is a thin lane-local shim that invokes `shared.cli`
- `boot_slice_request.json` records the committed lane-shaped request
- `boot_slice_response.json` records the expected deterministic response

This proof intentionally stays at `L1`. Native VSIX packaging, shell loading, and richer editor wiring remain deferred until a reproducible Visual Studio 2010 environment is available.
