# Xcode Companion Lane

This directory is the `companion` compatibility-technology lane for `apple.xcode`.

It is an AIDE architectural fallback for older Xcode families or workflows that exceed the documented XcodeKit source-editor surface. Exact version coverage is tracked in inventory and matrices.

P12 adds a runnable Apple companion proof through `cli-bridge` mode:

- `run_boot_slice.py` is a thin lane-local shim that invokes `shared.cli`
- `boot_slice_request.json` records the committed lane-shaped request
- `boot_slice_response.json` records the expected deterministic response

This proof reaches the accepted `L1` companion fallback shape. The native `xcodekit` lane remains blocked and is recorded separately.
