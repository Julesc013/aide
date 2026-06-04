# Rollback-Compatible Lifecycle Record Plan

## Record Shape

Rollback-compatible lifecycle records capture enough evidence to plan and review a future inverse operation. They are not rollback execution.

Required shape:

- `schema_version`
- `record_id`
- `lifecycle_plan_id`
- `transaction_or_operation_ids`
- `lifecycle_phase`
- `target_class`
- `path`
- `operation_type`
- `ownership_type`
- `preimage_hash`
- `preimage_content_ref`
- `postimage_hash`
- `postimage_content_ref`
- `inverse_operation`
- `rollback_preconditions`
- `rollback_stop_conditions`
- `manual_content_preservation_notes`
- `protected_path_checks`
- `validation_requirements_before_rollback`
- `evidence_refs`
- `review_gate`
- `unsupported_rollback_reasons`
- `rollback_execution_implemented`

## Preimage And Postimage Strategy

Records must store hashes directly and content snapshots only through safe content references. Snapshot policy must preserve manual content boundaries and must not include secrets. Preimage hashes block rollback planning when the observed file no longer matches the record.

## Inverse Operation Strategy

Inverse operations are descriptive until a later reviewed task implements rollback execution. The inverse operation must identify the affected path, ownership type, required preimage hash, expected restored hash, protected-path checks, and stop conditions.

## Unsupported Cases

Rollback remains unsupported for unknown ownership, manual content deletion, broad deletes, protected paths, path traversal, target-local truth replacement, branch/worktree changes, release publication, provider/model/Gateway/network effects, and any operation without enough preimage/postimage evidence.
