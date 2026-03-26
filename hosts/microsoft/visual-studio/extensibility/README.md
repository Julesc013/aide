# Visual Studio Extensibility Lane

This directory is the `extensibility` compatibility-technology lane for `microsoft.visual-studio`. It represents the modern VisualStudio.Extensibility SDK and related current contracts for late Visual Studio 2022 and Visual Studio 2026-era work.

P11 adds a runnable but deliberately conservative boot-slice proof through `cli-bridge` mode:

- `run_boot_slice.py` is a thin lane-local shim that invokes `shared.cli`
- `boot_slice_request.json` records the committed lane-shaped request
- `boot_slice_response.json` records the expected deterministic response

This proof reaches `L1` report-first depth only. The lane's documented `local-service` or out-of-process shape remains deferred until a real VisualStudio.Extensibility environment is introduced.
