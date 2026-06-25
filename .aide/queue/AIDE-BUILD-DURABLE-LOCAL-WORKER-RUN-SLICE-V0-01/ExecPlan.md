# AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01 ExecPlan

## Objective

Build the first durable local WorkerRun slice by composing accepted local
Service persistence, accepted local trust enforcement, and the accepted
fixture-backed LocalProcessExecutionHost.

## Scope

The implementation is limited to a new local Service slice module, an AIDE Lite
fixture/status/validate/reset command surface, focused tests, generated reports,
this task packet, queue index, and root plan/log updates.

## Design

- Evaluate accepted local trust records before invoking the host fixture.
- Consume the one-use local grant through the accepted local trust enforcement
  path.
- Launch the accepted local reference host once through its existing bounded
  path.
- Persist a WorkUnit, WorkerRun observation, host outcome, EvidencePacket, and
  EventRecord into an ephemeral SQLite local Service store.
- Append deterministic local Service events and record idempotency so replay
  resolves to the existing WorkerRun without another host launch.
- Store content-addressed artifact metadata in the local Service fixture state.

## Validation

Run focused durable WorkerRun tests, fixture/status/validate commands, local
trust/local Service/local process regressions, compileall, task inspect/evidence,
broad validation, diff checks, and leak scans.

## Result

PASS_WITH_WARNINGS. The proposed capability is
`durable_local_worker_run_slice_v0`; the next task is
`AIDE-CHECK-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01`.
