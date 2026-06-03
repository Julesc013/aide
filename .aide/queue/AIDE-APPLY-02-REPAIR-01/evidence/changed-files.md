# Changed Files

Task: `AIDE-APPLY-02-REPAIR-01`

## Queue And Status

- `.aide/queue/AIDE-APPLY-02-REPAIR-01/task.yaml`: created the repair WorkUnit for exactly the four `AIDE-CHECK-APPLY-02` findings.
- `.aide/queue/AIDE-APPLY-02-REPAIR-01/ExecPlan.md`: recorded the repair milestones, non-goals, and validation intent.
- `.aide/queue/AIDE-APPLY-02-REPAIR-01/prompt.md`: recorded the bounded prompt seed for the repair.
- `.aide/queue/AIDE-APPLY-02-REPAIR-01/status.yaml`: recorded `needs_review`, `PASS_WITH_WARNINGS`, and the repaired finding flags.
- `.aide/queue/AIDE-APPLY-02-REPAIR-01/evidence/changed-files.md`: this changed-file inventory.
- `.aide/queue/AIDE-APPLY-02-REPAIR-01/evidence/implementation-summary.md`: repair behavior summary.
- `.aide/queue/AIDE-APPLY-02-REPAIR-01/evidence/validation.md`: validation command log.
- `.aide/queue/AIDE-APPLY-02-REPAIR-01/evidence/boundary-confirmation.md`: allowed/protected/forbidden boundary evidence.
- `.aide/queue/AIDE-APPLY-02-REPAIR-01/evidence/remaining-risks.md`: remaining risk and warning classification.
- `.aide/queue/AIDE-APPLY-02-scoped-transaction-executor-v0/task.yaml`: moved AIDE-APPLY-02 to `repaired_needs_review` pending recheck.
- `.aide/queue/AIDE-APPLY-02-scoped-transaction-executor-v0/status.yaml`: recorded repair completion and next checkpoint.
- `.aide/queue/AIDE-APPLY-02-scoped-transaction-executor-v0/ExecPlan.md`: added repair progress note.
- `.aide/queue/index.yaml`: registered `AIDE-APPLY-02-REPAIR-01` and updated AIDE-APPLY-02 queue summary.

## Executor, Tests, Schema, Policy, And Docs

- `core/apply/transaction_executor.py`: added resolved-path containment checks, apply-mode multi-mutating-operation blocking, resolved output path validation, prewrite revalidation, and persisted `report_path`/`rollback_record_path`.
- `core/apply/tests/test_transaction_executor.py`: added tests for resolved symlink/reparse escape, protected resolved targets, multi-mutating apply blocking, multi-operation dry-run, and persisted report path schema behavior.
- `.aide/scripts/tests/test_aide_apply_02_scoped_transaction_executor.py`: added a command-level test proving the checked-in dry-run example runs and does not mutate the fixture.
- `.aide/examples/apply/scoped-transaction-executor.dry-run.example.json`: updated checked-in example preimage and postimage hashes to match the current fixture.
- `.aide/apply/transaction-executor-report.schema.json`: added optional `report_path` and `rollback_record_path`.
- `.aide/policies/scoped-transaction-executor.yaml`: recorded repair boundary flags for resolved paths, multi-mutating apply blocking, and persisted report path requirement.
- `docs/reference/scoped-transaction-executor.md`: documented resolved-path safety, v0 multi-mutating apply blocking, and report path persistence.
- `core/apply/README.md`: documented the repaired v0 constraints.

## Generated Reports

The following generated reports were refreshed by validation/status commands and retained because the repair task allowed report outputs:

- `.aide/reports/scoped-transaction-executor-example-report.json`
- `.aide/reports/scoped-transaction-executor-example-rollback.json`
- `.aide/reports/scoped-transaction-executor-fixture-plan.md`
- `.aide/reports/scoped-transaction-executor-fixture-report.md`
- `.aide/reports/scoped-transaction-executor-status.md`
- `.aide/reports/scoped-transaction-executor-validation.md`
- `.aide/reports/managed-section-status.md`
- `.aide/reports/managed-section-next-plan.md`
- `.aide/reports/managed-section-fixture-plan.json`
- `.aide/reports/managed-section-fixture-plan.md`
- `.aide/reports/managed-section-fixture-validation.md`
- `.aide/reports/managed-section-conflict-report.md`
- `.aide/reports/transaction-model-status.md`
- `.aide/reports/transaction-safety-gates.md`
- `.aide/reports/transaction-next-plan.md`
- `.aide/reports/transaction-fixture-plan.json`
- `.aide/reports/transaction-fixture-plan.md`
- `.aide/reports/transaction-fixture-validation.md`
- `.aide/reports/current-aide-roadmap.md`
- `.aide/reports/task-os-command-status.md`
- `.aide/reports/task-os-task-status.md`
