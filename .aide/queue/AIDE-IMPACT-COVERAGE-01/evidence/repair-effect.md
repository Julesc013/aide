# Failed source attempt and bounded fixture repair

Allocation1 4cca8a9f445a43b7b20f092ee8d0ff87 ran13 methods:12 pass,1 fail,
zero errors/skips. All seven new regressions and the original/candidate missing-base
comparison passed. Collection hashes verified; retired/quiescent, scratch absent,
reservation released. Full original receipt/output retained without reinterpretation.

Static trace: original alias test submits a _write_minimal_repo scaffold containing
queue/index.yaml but no managed_workspace.py. source_maintainer_job_guard explicitly
refuses that shape. Its returned output was captured by the test and not included
in the assertion, so this is a source-traced diagnosis, not a captured refusal.
Correct only the test subject to the actual admitted source or validated exported
root. Keep all original acceptance assertions; add captured output to any failure.
The internal selftest still uses its original temporary fixtures and all assertions.
No guard bypass, mocks, skipped checks or product permission changes.

Request review of this fixture correction and one existing capability ledger refresh
before the next candidate is frozen. The command is `py -3 -B .aide/scripts/aide_lite.py
capability ledger`; only the four allowed capability reports may change. Preserve
preimages and verify capability classification remains identical and binding CURRENT.
This authorizes no job. Prepare a later exact reviewed allocation2 combining full
source13 checks first, then existing export-owner6 and delivered13 in fresh processes.
Stop before export on any source failure. Allocation3 remains the fixed-range preview;
ceiling3 unchanged. No automatic retry, resource increase or additional allocation.
