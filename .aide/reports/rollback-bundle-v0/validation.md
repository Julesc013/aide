# RollbackBundle v0 Validation

- result: `PASS_WITH_WARNINGS`
- proposed_capability: `rollback_bundle_v0`
- recommended_next_task: `AIDE-CHECK-ROLLBACK-BUNDLE-V0-01`
- error_count: 0

## Checks

- candidate_distribution_bound: `true`
- candidate_project_lock_bound: `true`
- cli_registered: `true`
- fixture_matrix_passed: `true`
- helper_exists: `true`
- install_apply_not_implemented: `true`
- install_record_bound: `true`
- ownership_ledger_bound: `true`
- prior_project_lock_bound: `true`
- rollback_apply_not_implemented: `true`
- rollback_bundle_generated: `true`
- rollback_bundle_valid: `true`
- schema_alignment: `true`
- schema_exists: `true`
- source_distribution_bound: `true`
- source_output_not_target_truth: `true`
- target_repository_mutation_not_implemented: `true`
- uninstall_apply_not_implemented: `true`
- update_apply_not_implemented: `true`
- update_plan_accepted: `true`
- update_plan_bound: `true`

## Warnings

- RollbackBundle v0 is proposed until independent check and acceptance.
- RollbackBundle records rollback preparation metadata only and performs no rollback apply.
- UpdateReceipt remains a future dependency after acceptance.
