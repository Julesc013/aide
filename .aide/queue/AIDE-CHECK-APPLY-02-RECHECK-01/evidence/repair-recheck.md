# Repair Recheck

Task: `AIDE-CHECK-APPLY-02-RECHECK-01`

## Finding 1: Runnable Dry-Run Example

Status: closed.

Evidence:

- `.aide/examples/apply/scoped-transaction-executor.dry-run.example.json` now contains current fixture preimage and postimage hashes.
- `.aide/scripts/tests/test_aide_apply_02_scoped_transaction_executor.py` includes `test_checked_in_dry_run_example_passes_and_preserves_fixture`.
- `.aide/reports/scoped-transaction-executor-example-report.json` records `status: PASS`, `result: PASS`, `target_files_mutated: false`, and `report_path`.

Validation:

- `py -3 .aide/scripts/aide_lite.py scoped-transaction run --plan .aide/examples/apply/scoped-transaction-executor.dry-run.example.json`: PASS.
- Command-level tests: PASS.

Residual risk: none blocking. The example remains dry-run/report mode and does not weaken preimage hash or postimage verification.

## Finding 2: Resolved Symlink/Reparse-Point Safety

Status: closed.

Evidence:

- `core/apply/transaction_executor.py` validates lexical path containment and then resolves target/output paths through `_resolved_path_result`.
- Resolved paths outside repo, outside allowed roots, or inside protected roots block with `BLOCKED_RESOLVED_PATH_ESCAPE`.
- Apply mode revalidates resolved targets before writing.
- Tests cover symlink file escape, symlink parent escape, resolved protected path, and valid path predicate behavior.

Validation:

- `py -3 -m unittest core.apply.tests.test_transaction_executor`: PASS; symlink tests ran on this platform.
- Scoped transaction fixture validation remains PASS for valid fixture paths.

Residual risk: platform-specific reparse behavior should remain under review before target-repo use, but v0 evidence is sufficient for core repo scoped acceptance with notes.

## Finding 3: Multi-Operation Apply Partial Mutation Risk

Status: closed.

Evidence:

- Apply mode blocks more than one mutating staged change before any write with `BLOCKED_MULTI_OPERATION_APPLY_NOT_ATOMIC`.
- Multi-operation dry-run remains non-mutating.
- Docs explicitly state v0 does not provide multi-file atomic apply.
- Rollback execution was not introduced.

Validation:

- `test_multi_mutating_apply_is_blocked_before_mutation`: PASS.
- `test_multi_operation_dry_run_remains_non_mutating`: PASS.
- Single-operation apply behavior remains covered by the existing unit suite.

Residual risk: multi-file atomic apply is deferred by design.

## Finding 4: Direct Core Persisted `report_path`

Status: closed.

Evidence:

- `write_available_outputs` assigns `rollback_record_path` and `report_path` before serializing the final report.
- Report schema permits `report_path` and `rollback_record_path`.
- Direct core output test loads persisted report and confirms `report_path`.
- CLI-generated example report includes `report_path`.

Validation:

- `test_final_report_and_evidence_outputs_are_generated`: PASS.
- Checked-in example command report includes `.aide/reports/scoped-transaction-executor-example-report.json`.

Residual risk: none blocking. The report schema remains permissive with `additionalProperties: true`, which is acceptable for v0 but should be revisited before broader apply surfaces.
