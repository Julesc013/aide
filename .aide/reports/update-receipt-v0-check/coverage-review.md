# Coverage Review

## Required Fields

The schema/helper/report surfaces model and validate:

- `update_receipt_ref`
- `update_plan_ref`
- `rollback_bundle_ref`
- `target_project_ref`
- `old_project_lock_ref`
- `new_project_lock_ref`
- `prior_install_record_refs`
- `new_install_record_ref`
- `prior_ownership_ledger_ref`
- `new_ownership_ledger_ref`
- `source_distribution_ref`
- `candidate_distribution_ref`
- `operation_receipts`
- `skipped_operations`
- `failed_operations`
- `changed_file_refs`
- `changed_section_refs`
- `preimage_digests`
- `postimage_digests`
- `artifact_refs`
- `validation_results`
- `approval_ref`
- `executor_ref`
- `execution_environment`
- `warnings`
- `limitations`
- `risk_class`
- `evidence_refs`
- `explicit_non_capabilities`
- `created_at`
- `created_by`
- `extensions`

## Operation Classes

All 23 operation receipt classes are represented in schema/helper validation. Fixture data includes 21 of 23 as positive receipt rows. Missing positive fixture rows are `manual_review_recorded` and `operation_failed`.

## Skipped Reasons

All 18 skipped-operation reasons are represented in helper validation. Fixture data includes 8 of 18 as skipped rows. Missing positive skipped rows are `case_collision`, `missing_approval`, `missing_rollback_requirement`, `policy_refusal`, `postimage_mismatch`, `preimage_mismatch`, `symlink_or_reparse_uncertainty`, `unknown_required_feature`, `unsupported_operation`, and `validation_failed`.

## Disposition

The coverage gap is warning-class because semantic validation covers the enum surfaces and the required fixture set is present. No material finding was opened.
