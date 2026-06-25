# Local Service Foundation Validation

- status: PASS_WITH_WARNINGS
- validated: true
- recommended_next_task: AIDE-CHECK-LOCAL-SERVICE-FOUNDATION-V0-01

## Checks

- migration_idempotent: PASS
- future_migration_refused: PASS
- object_put_get_list: PASS
- resource_version_conflict_refused: PASS
- atomic_object_event_committed: PASS
- rollback_on_error: PASS
- monotonic_events: PASS
- at_least_once_only: PASS
- artifact_write_read: PASS
- artifact_deduplicated: PASS
- artifact_digest_mismatch_refused: PASS
- artifact_path_traversal_refused: PASS
- idempotency_duplicate: PASS
- idempotency_conflict_refused: PASS
- reopen_persistence: PASS
- corruption_refused: PASS
- source_checkout_unchanged: PASS
- false_boundaries: PASS
