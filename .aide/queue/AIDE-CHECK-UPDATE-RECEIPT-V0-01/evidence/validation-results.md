# Validation Results

Result: `PASS_WITH_WARNINGS`

Passed:

- JSON schema parse
- `py_compile`
- `compileall`
- focused UpdateReceipt tests
- `update-receipt status`
- `update-receipt project`
- `update-receipt validate`
- predecessor status/project/validate commands
- Q43-Q48 no-apply/no-publish validators
- broad AIDE validation
- source build task inspect/evidence
- hygiene scans
- `git diff --check`
- `git diff --cached --check`

Observed UpdateReceipt validation facts:

- `update_receipt_valid: true`
- `schema_alignment: true`
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

Warning:

- Some enum members are validator/schema-covered rather than each being represented by a distinct positive fixture row.
