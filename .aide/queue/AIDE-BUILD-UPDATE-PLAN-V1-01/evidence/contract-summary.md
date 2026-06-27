# Contract Summary

UpdatePlan v1 models:

- `update_plan_ref`
- target project identity
- current and candidate ProjectLock refs/digests
- candidate DistributionManifest ref/digest
- OwnershipLedger ref/digest
- InstallRecord refs/digests
- MigrationRecord refs/digests
- planned operations
- preserved paths
- managed file updates
- managed section updates
- conflicts
- manual review items
- validation plan
- rollback requirements
- risk class
- approval requirements
- evidence refs
- explicit non-capabilities
- required/optional features
- extensions

Planned operation classes:

- `add_managed_file`
- `update_managed_file`
- `remove_managed_file`
- `add_managed_section`
- `update_managed_section`
- `remove_managed_section`
- `preserve_project_owned`
- `preserve_project_overlay`
- `preserve_local_only`
- `preserve_runtime_generated`
- `preserve_evidence_only`
- `preserve_legacy`
- `regenerate_project_output`
- `manual_review_required`
- `refuse`

The validator fails closed for unsafe ownership, never-touch updates, unknown ownership updates, case collisions, symlink/reparse uncertainty, unsafe paths, predecessor mismatches, missing rollback requirements, unknown required features/extensions, source-output-as-target-truth, apply claims, and target mutation claims.
