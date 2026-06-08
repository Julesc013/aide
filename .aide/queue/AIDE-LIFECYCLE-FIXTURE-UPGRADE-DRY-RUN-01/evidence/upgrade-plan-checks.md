# Upgrade Plan Checks

Result: `PASS_WITH_WARNINGS`

Plans checked:

- `upgrade-v2`
- `upgrade-manual-preserved`
- `drift-detected`

All three generated upgrade plans parse and preserve:

- lifecycle phase `upgrade`
- mode `dry-run` or `report`
- `target_class=fixture`
- explicit operation list
- explicit operation allowlist
- explicit allowed roots
- explicit protected roots
- explicit prohibited operation checks
- `target_files_mutated_expected=false`
- `target_files_mutated=false`
- `lifecycle_apply_executed=false`
- `scoped_transaction_apply_executed=false`
- `rollback_execution_implemented=false`
- `review_gate=needs_review`

Warning:

- `upgrade-manual-preserved` has no static `expected_report_ref`; generated plan report evidence exists.

Detailed machine-readable evidence:

- `.aide/reports/lifecycle-fixture-upgrade-dry-run/upgrade-plan-checks.json`
- `.aide/reports/lifecycle-fixture-upgrade-dry-run/upgrade-scenario-matrix.json`
