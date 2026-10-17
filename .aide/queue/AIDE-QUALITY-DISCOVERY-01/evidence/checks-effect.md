# First managed allocation

Execute run_checks.py once using checks-job-template.json. Freeze reviewed tree
as a byte-identical structured commit; substitute only its actual commit/tree in
the template. Existing input hashes and Python digest must match immediately
before launch, with clean checkout and existing shared runner admission.

Original Q37/Q38 methods and seven new CLI/behavior methods use disposable TEMP
under the existing managed job. No canonical outputs, network, models, target
repository, live report generation or native worker delivery. Expected 23 methods
(Q37 count must be enumerated by the runner, not silently skipped); exact observed
IDs and counts retained. No skips or failures accepted. Allocation one of three.

Existing limits/config and D roots unchanged. Retain stdout/stderr, test IDs,
inputs, measured peaks and result; verify collected digests, child quiescence,
scratch retirement and reservation release. Failure remains original evidence;
no automatic retry. Previous unrelated runtime qualification is reused unchanged.
