# Installed Codex executable under the existing Windows Job

Date: 2026-09-29. WorkUnit: `AIDE-CODEX-DISPATCH-GATE-01`.

Test-only commit `6e21e70f4c329d0a137c56a19f32a9030d78df43`, tree `86734c9256643428404f1456a092ff27d70b6969`, adds one Windows test in `.aide/scripts/tests/test_continuous_worker_pipeline.py`. It starts the installed `codex --version` through `WindowsJobHost`, then checks suspended-child and resume callbacks, exit 0, quiescence and CLI output. The checked executable was `codex-cli 0.145.0`, SHA-256 `83751f15cb6a0a7b97df67752c001e3fe1c20e18ffbfec3ff63567296205eb6c`. No model command was issued. Production `core/runtime/continuous_worker/**` has no diff from independently accepted `a8c9935e`.

The configured D runner executed `python -m unittest discover -s .aide/scripts/tests -p test_continuous_worker_pipeline.py -v`: **32/32 PASS**, exit 0. Job `cbfbffa276fa49dbaaa41a312f474b4e`, manifest digest `85a86a594c7bf4f4a45a1b78ad99fa75fd3a30498f9b8bf3fcdabd2f3cb712c0`, retained receipt SHA-256 `516906773abd7c91fe3033780eb3cc3d709aa35788bb9580870f2f5f59e8b6eb`. Peak memory was 126857216 bytes, peak scratch 661653 bytes; scratch was absent, reservation released and runner control had no active job after completion. The retained log says `Ran 32 tests`, `OK`.

This establishes installed executable launch compatibility within the owned Job. It does not qualify a model turn, actual pause of a real Codex inference, token accounting, exported Lite or stable publication. Those gates remain open.
