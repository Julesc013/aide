# Rollback Dry-Run Design

This WorkUnit is a static report-only / dry-run rollback planning check. It does not implement rollback apply and does not execute rollback apply.

Inputs:

- `.aide/apply/lifecycle-rollback-record.schema.json`
- `.aide/examples/apply/lifecycle/lifecycle-rollback-record.example.json`
- `.aide/examples/apply/lifecycle-fixtures/rollback-records/install-managed-section.rollback.json`
- `.aide/examples/apply/lifecycle-fixtures/rollback-records/upgrade-v2.rollback.json`
- `.aide/examples/apply/lifecycle-fixtures/generated-plans/rollback-record-generated.plan.json`
- `.aide/examples/apply/lifecycle-fixtures/generated-plans/install-managed-section.plan.json`
- `.aide/examples/apply/lifecycle-fixtures/generated-plans/upgrade-v2.plan.json`
- `.aide/examples/apply/lifecycle-fixtures/expected-reports/rollback-record-generated.report.json`
- `.aide/examples/apply/lifecycle-fixtures/expected-reports/install-managed-section.report.json`
- `.aide/examples/apply/lifecycle-fixtures/expected-reports/upgrade-v2.report.json`

Checks:

- schema/version and required-field checks;
- rollback record reference checks;
- current hash and postimage hash checks for fixture records;
- inverse operation checks;
- precondition and stop condition checks;
- manual preservation checks;
- protected path checks;
- scoped executor v0 interlock checks;
- no rollback execution, no uninstall execution, no lifecycle apply execution, no scoped transaction fixture apply, no target_files_mutated proof.

Result: `PASS_WITH_WARNINGS`. The warnings are that the generic rollback example is placeholder-only and rollback records remain static compatibility evidence, not executable rollback authority.
