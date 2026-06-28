# Accepted Operation Classes

Accepted operation classes are limited to the fixture executor's current allowlist:

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
- `manual_review_required`
- `refuse`

Write operation classes require rollback coverage in the accepted fixture model.

This acceptance does not add support for `regenerate_project_output`, arbitrary command execution, target-local scans, real target writes, source-change apply, DevelopmentTransaction apply, PatchTransaction apply, or release/publication operations.
