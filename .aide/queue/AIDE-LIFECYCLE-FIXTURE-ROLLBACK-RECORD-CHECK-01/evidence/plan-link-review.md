# Plan Link Review

Result: `PASS`

Generated plans checked: 13

Expected reports checked: 7

Rollback links:

- `.aide/examples/apply/lifecycle-fixtures/generated-plans/install-managed-section.plan.json` links to `.aide/examples/apply/lifecycle-fixtures/rollback-records/install-managed-section.rollback.json`.
- `.aide/examples/apply/lifecycle-fixtures/generated-plans/upgrade-v2.plan.json` links to `.aide/examples/apply/lifecycle-fixtures/rollback-records/upgrade-v2.rollback.json`.
- `.aide/examples/apply/lifecycle-fixtures/generated-plans/rollback-record-generated.plan.json` links to `.aide/examples/apply/lifecycle-fixtures/rollback-records/install-managed-section.rollback.json`.
- `.aide/examples/apply/lifecycle-fixtures/expected-reports/install-managed-section.report.json` references the install rollback record.
- `.aide/examples/apply/lifecycle-fixtures/expected-reports/upgrade-v2.report.json` references the upgrade rollback record.
- `.aide/examples/apply/lifecycle-fixtures/expected-reports/rollback-record-generated.report.json` references the install rollback record.

Bidirectional reference result: PASS for fixture rollback records. Both fixture rollback records are linked from generated plans and expected reports.

Mutation/execution claim result: PASS. Linked plans and reports preserve `target_files_mutated=false`, `lifecycle_apply_executed=false`, `scoped_transaction_apply_executed=false`, `rollback_execution_implemented=false`, and empty `files_changed` where reports expose that field.

Defects: none.
