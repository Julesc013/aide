# Implementation Summary

Implemented command group:

- `py -3 .aide/scripts/aide_lite.py lifecycle-fixture status`
- `py -3 .aide/scripts/aide_lite.py lifecycle-fixture run --scenario install-managed-section --mode apply-temp`
- `py -3 .aide/scripts/aide_lite.py lifecycle-fixture verify`

Implemented module:

- `core/apply/lifecycle_fixture_runner.py`

Internal seams:

- `ScenarioLoader`
- `TransactionCompiler`
- `ScopedExecutor`
- `FixtureVerifier`
- `EvidenceReporter`

Supported slice:

- scenario: `install-managed-section`
- mode: `apply-temp`
- operation: `update_managed_section`
- mutation scope: temp workspace only

The runner reads the canonical lifecycle fixture plan and target/expected files,
copies the target fixture tree to `.aide/reports/lifecycle-fixture-runner/workspaces/latest`,
applies the marker-bounded managed-section replacement to the temp copy only,
verifies hashes and manual content preservation, writes a rollback-compatible
record, and emits run/verify/future/unfinished reports.

`aide_lite.py` contains command parsing and dispatch only. Runner behavior lives
in `core/apply/lifecycle_fixture_runner.py`.
