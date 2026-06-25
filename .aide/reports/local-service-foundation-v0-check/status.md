# Local Service Foundation v0 Check

- status: PASS_WITH_WARNINGS
- checked_task: AIDE-BUILD-LOCAL-SERVICE-FOUNDATION-V0-01
- checked_capability: local_service_foundation_v0
- material_finding_count: 0
- missing_evidence: 0
- recommended_next_task: AIDE-ACCEPT-LOCAL-SERVICE-FOUNDATION-V0-01

## Assertions

- source.task_chain: PASS
- cli.init_fixture_boundary: PASS
- migrations.idempotent_schema: PASS
- objects.versioned_put_get_list: PASS
- events.atomic_monotonic_cursor: PASS
- idempotency.duplicate_conflict: PASS
- artifacts.cas_integrity: PASS
- restart.persistence: PASS
- migrations.future_refusal: PASS
- health.corruption_refusal: PASS
- local_state.absent: PASS
