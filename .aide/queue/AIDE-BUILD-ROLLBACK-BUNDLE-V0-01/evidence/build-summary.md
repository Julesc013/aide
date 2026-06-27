# Build Summary

Built `rollback_bundle_v0` as a no-apply rollback-preparation protocol slice.

The build adds:

- RollbackBundle v0 JSON Schema.
- Deterministic helper/projection/validation logic.
- AIDE Lite `rollback-bundle status`, `project`, and `validate` commands.
- Valid and invalid fixture corpus for reverse-operation and fail-closed behavior.
- Focused tests.
- Generated status, projection, validation, fixture matrix, reverse-operation summary, limitations, and no-apply boundary reports.

The build records reverse operation classes as plans only:

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
