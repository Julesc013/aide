# AIDE-BUILD-LOCAL-SERVICE-FOUNDATION-V0-01 ExecPlan

## Objective

Implement a minimal local Service foundation with SQLite-backed objects,
events, artifact metadata, idempotency records, and cursors plus a filesystem
content-addressed artifact store.

## Scope

Implementation is limited to `core/service/**`, AIDE Lite fixture commands,
focused tests, generated reports, this task packet, queue index, and root
plan/log updates.

## Design

- SQLite stores migrations, objects, trust-bearing event records, artifact
  metadata, idempotency records, and subscription cursors.
- Filesystem content-addressed storage writes verified payload bytes before
  metadata is recorded.
- Fixture commands use temporary state by default.
- Delivery semantics are explicitly at-least-once, not exactly-once.
- The slice implements no network listener, scheduler, worker execution,
  capability execution, trust enforcement, MCP, Workbench, provider/model calls,
  preview/apply/rollback, mutation, release, or promotion.

## Validation

Run focused local service tests, fixture commands, validation commands,
compileall, local-process/trust regressions, task inspect/evidence, broad
validation, diff checks, and leak scans.

## Result

PASS_WITH_WARNINGS. The proposed capability is
`local_service_foundation_v0`; the next task is
`AIDE-CHECK-LOCAL-SERVICE-FOUNDATION-V0-01`.
