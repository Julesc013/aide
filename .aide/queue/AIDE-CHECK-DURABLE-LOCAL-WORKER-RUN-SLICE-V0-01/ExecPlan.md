# AIDE-CHECK-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01 ExecPlan

## Objective

Independently check the completed durable local WorkerRun build without
repairing production code or widening the accepted local runtime boundary.

## Scope

Allowed edits are limited to this check task packet, its evidence directory,
the check report directory, the queue index, and root plan/log entries.

## Method

- Verify source-chain and queue consistency for the build task and accepted
  prerequisites.
- Run a task-local independent harness that invokes the durable fixture as the
  system under test with `write_reports=False`.
- Inspect the temporary SQLite state, events, idempotency rows, artifact
  metadata, raw event stream, and committed build reports with independent
  parsing.
- Check explicit false-boundary fields and warning truthfulness.
- Classify any defect as material only when it affects evidence truthfulness,
  durable WorkerRun semantics, read-only safety, authority boundaries, or
  advertised capability scope.

## Validation

Run the independent harness, task inspect/evidence, focused durable tests,
durable status/validate, broad AIDE validation, diff checks, leak scans, and
commit-policy validation.

## Stop Condition

Stop at `needs_review`. If material findings remain, recommend exactly
`AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-REPAIR-01`; otherwise recommend
exactly `AIDE-ACCEPT-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01`.
