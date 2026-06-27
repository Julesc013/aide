# Accepted Operation Classes

UpdatePlan v1 accepts the following dry-run operation classes:

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

These operation classes describe planned intent only. They do not authorize writes, deletes, managed-section edits, target scans, or repository mutation.
