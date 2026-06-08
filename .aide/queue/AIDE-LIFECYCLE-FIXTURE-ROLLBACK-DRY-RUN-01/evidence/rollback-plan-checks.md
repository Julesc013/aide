# Rollback Plan Checks

Report: `.aide/reports/lifecycle-fixture-rollback-dry-run/rollback-plan-checks.json`

Result: `PASS_WITH_WARNINGS`

Plans checked:

- `.aide/examples/apply/lifecycle-fixtures/generated-plans/rollback-record-generated.plan.json`
- `.aide/examples/apply/lifecycle-fixtures/generated-plans/install-managed-section.plan.json`
- `.aide/examples/apply/lifecycle-fixtures/generated-plans/upgrade-v2.plan.json`

Findings:

- `rollback-record-generated` is `phase=rollback`, `mode=report`, `target_class=fixture`, and points at the install rollback record destination.
- `install-managed-section` is `phase=install`, `mode=dry-run`, `target_class=fixture`, and points at the install rollback record.
- `upgrade-v2` is `phase=upgrade`, `mode=dry-run`, `target_class=fixture`, and points at the upgrade rollback record.
- All checked plans preserve `target_files_mutated=false`, `rollback_execution_implemented=false`, `lifecycle_apply_executed=false`, and `scoped_transaction_apply_executed=false`.

No generated lifecycle fixture plan was mutated.
