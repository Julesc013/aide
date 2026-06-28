# Validation Results

Result: `ACCEPTED_WITH_WARNINGS`

Passed:

- focused UpdateReceipt tests
- `update-receipt status`
- `update-receipt project`
- `update-receipt validate`
- predecessor regressions
- Q43-Q48 no-apply/no-publish validators
- broad AIDE validation
- build/check/acceptance task inspect/evidence
- safety scans
- `git diff --check`
- `git diff --cached --check`

Accepted validation facts:

- `update_receipt_valid: true`
- `fixture_matrix_passed: true`
- `rollback_bundle_accepted: true`
- `update_plan_bound: true`
- `rollback_bundle_bound: true`
- `source_distribution_bound: true`
- `candidate_distribution_bound: true`
- `old_project_lock_bound: true`
- `new_project_lock_bound: true`
- `ownership_ledger_bound: true`
- `install_record_bound: true`
- `update_apply_not_implemented: true`
- `target_repository_mutation_not_implemented: true`
- `distribution_apply_engine_not_started: true`
- `source_output_not_target_truth: true`
- `error_count: 0`

Warnings are recorded in `warning-dispositions.md`.
