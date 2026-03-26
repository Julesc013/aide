# Visual Studio For Mac Companion Lane

This directory is the `companion` compatibility-technology lane for `microsoft.visual-studio-mac`. It is an AIDE fallback for adjacent or archival workflows around a retired host family, not a literal Microsoft extensibility product name.

P11 adds the first runnable Microsoft companion proof through `cli-bridge` mode:

- `run_boot_slice.py` is a thin lane-local shim that invokes `shared.cli`
- `boot_slice_request.json` records the committed lane-shaped request
- `boot_slice_response.json` records the expected deterministic response

This proof reaches the accepted `L1` companion fallback shape. The native MonoDevelop-derived lane remains blocked and is recorded separately.
