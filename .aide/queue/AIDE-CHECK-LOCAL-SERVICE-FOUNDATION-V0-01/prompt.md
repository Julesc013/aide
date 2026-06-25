# Prompt

Create and process `AIDE-CHECK-LOCAL-SERVICE-FOUNDATION-V0-01`.

This is a check-only task. Verify `AIDE-BUILD-LOCAL-SERVICE-FOUNDATION-V0-01`
without repairing implementation or accepting `local_service_foundation_v0`.

Verify local state remains ignored, migrations are deterministic and
idempotent, future migrations are refused, object/event writes are atomic,
resource-version conflicts fail closed, events are monotonic and at-least-once
only, cursors resume, idempotency works, artifacts are content-addressed and
payload-before-metadata, path containment holds, restart persistence works,
corruption is refused, tests and broad validation pass, reports are scrubbed,
and the slice implements no network, scheduler, worker/model/provider behavior,
trust enforcement, Workbench, MCP, preview/apply/rollback, mutation, GitHub,
release, or promotion behavior.

If material findings remain, recommend
`AIDE-BUILD-LOCAL-SERVICE-FOUNDATION-V0-REPAIR-01`.

If the check passes, recommend
`AIDE-ACCEPT-LOCAL-SERVICE-FOUNDATION-V0-01`.
