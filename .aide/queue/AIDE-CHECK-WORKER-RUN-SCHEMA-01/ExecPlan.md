# ExecPlan: AIDE-CHECK-WORKER-RUN-SCHEMA-01

## Objective

Independently verify the `minimal_worker_run_schema` slice from `AIDE-BUILD-WORKER-RUN-SCHEMA-01`.

## Scope

- Review WorkerRun helper, schema, CLI dispatch, tests, projections, reports, and build evidence.
- Verify compatibility with accepted lifecycle fixture, contract envelope, EvidencePacket, WorkUnit Queue, read-only WorkUnit CLI, and WorkUnit mutation CLI layers.
- Run focused tests and negative fail-closed checks.
- Produce check evidence and `.aide/reports/worker-run-check/check-report.*`.

## Non-Goals

No implementation repair, worker execution, WorkUnit claim/run/finish/repair, leases, scheduler, supervisor, provider adapters, TestJob, Test Broker, Service, Commander, branch/worktree automation, target apply, active apply, rollback execution, release, promotion, network, Gateway, GitHub, or model/provider calls.

## Stop State

End at `needs_review`.
