# Canonical Fixture Preservation

`distribution-apply verify` hashes canonical scenario files before and after each temporary execution.

Observed result:

- canonical_fixture_unchanged: `true`
- temp_workspace_retained: `false`
- source_repo_apply_occurred: `false`
- real_target_repo_modified: `false`

The engine writes candidate file changes, managed-section changes, generated receipt outputs, and rollback verification state only inside temporary workspace copies.
