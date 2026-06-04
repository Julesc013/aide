# Fixture Validation Evidence

Static validation scope:

- JSON fixture metadata parses locally.
- Lifecycle expected report examples use `aide.lifecycle-report.v0`.
- Rollback-compatible record examples use `aide.lifecycle-rollback-record.v0`.
- Protected path attempts are represented as metadata only.
- Traversal and broad-delete attempts are represented as metadata only.
- Target files are static checked-in fixture artifacts.
- `target_files_mutated` is false in expected reports and validation reports.
- `lifecycle_apply_executed` is false in fixture metadata.

Validator interlock:

- Existing `lifecycle-schema status`: PASS.
- Existing `lifecycle-schema validate`: PASS.
- Existing `lifecycle-schema fixture-verify`: PASS.
- Validator code was not changed; physical fixture tree validation is local parse/evidence work until a future check or validator-coverage task widens that scope.
