# Accepted Contract

Accepted predecessor dependencies:

- `distribution_manifest_v1`
- `project_lock_v0`
- `ownership_ledger_v1`
- `install_record_v0`
- `migration_record_v0`
- `update_plan_v1`

Accepted modeled fields:

- `rollback_bundle_ref`
- `update_plan_ref`
- `target_project_ref`
- `prior_project_lock_ref`
- `candidate_project_lock_ref`
- `prior_install_record_refs`
- `prior_ownership_ledger_ref`
- `source_distribution_ref`
- `candidate_distribution_ref`
- `preimage_artifact_refs`
- `managed_file_preimages`
- `managed_section_preimages`
- `reverse_operations`
- `operation_rollback_map`
- `validation_plan`
- `integrity_checks`
- `manual_review_items`
- `limitations`
- `risk_class`
- `evidence_refs`
- `explicit_non_capabilities`
- `created_at`
- `created_by`
- `extensions`

Accepted reverse operation classes:

- `restore_managed_file_preimage`
- `restore_managed_section_preimage`
- `remove_added_managed_file`
- `remove_added_managed_section`
- `restore_project_lock`
- `restore_install_record`
- `restore_ownership_ledger`
- `regenerate_project_output`
- `manual_review_required`
- `rollback_unavailable`
- `refuse`

Accepted limitation model:

- limitations must be explicit, evidenced, and bound to the accepted UpdatePlan context;
- `manual_review_required` records cases needing human decision before later apply work;
- `rollback_unavailable` is a limitation record, not permission to apply without recovery;
- conflict-only or limitation-only bundles may pass with warnings when they preserve the no-apply boundary.
