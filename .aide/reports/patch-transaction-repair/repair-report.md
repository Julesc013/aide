# PatchTransaction Repair Report

- task_id: `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01`
- status: `PASS_WITH_WARNINGS`
- repair_scope: `patch-transaction-path-scope-fail-closed`
- failed_check_task_id: `AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01`
- repaired_task_id: `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01`
- material_findings_repaired:
  - `path_scope_drive_prefixed_relative_accepted`
  - `path_scope_duplicate_normalization_accepted`
- schema_changed: `false`
- projection_boundary_changed: `false`
- policy_evaluation_performed: `false`
- approval_granted: `false`
- apply_performed: `false`
- target_mutated: `false`
- rollback_performed: `false`
- trusted: `false`
- recommended_next_task: `AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-REPAIR-01`

## Summary

The repair changes only PatchTransaction path-scope validation and focused
tests. Drive-prefixed relative paths are now rejected, and duplicate-normalized
path declarations now fail as ambiguous. The schema-only no-apply boundary is
unchanged.
