# Adversarial Probes

Committed fixture scenarios checked:

- `missing-update-plan-binding`
- `missing-rollback-bundle-binding`
- `mismatched-update-plan-rollback-bundle`
- `predecessor-source-distribution-mismatch`
- `predecessor-project-lock-mismatch`
- `predecessor-ownership-ledger-mismatch`
- `predecessor-install-record-mismatch`
- `predecessor-migration-record-mismatch`
- `run-without-accepted-context`

Each returned:

- `status: FAILED_VALIDATION`
- expected explicit `refusal_code`
- `update_receipt_generated: false`
- `operation_count: 0`
- `temp_workspace_digest_before: null`
- `canonical_fixture_unchanged: true`
- `real_target_repo_modified: false`
- `source_repo_apply_occurred: false`

Direct validator probes checked:

- non-accepted context status refuses with `distribution_apply_engine.accepted_context_not_accepted`
- operation not in UpdatePlan refuses with `distribution_apply_engine.operation_not_in_update_plan`
- operation lacking RollbackBundle coverage refuses with `distribution_apply_engine.operation_lacks_rollback_coverage`
