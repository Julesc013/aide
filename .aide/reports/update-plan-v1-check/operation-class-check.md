# Operation Class Check

All required operation classes are represented in both the schema enum and helper-supported operation set:

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

The check-local probe validated each operation class in a valid context. The live projected plan does not contain every possible operation class, which is expected because it is one concrete dry-run projection, not an exhaustive operation catalog.
