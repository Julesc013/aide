# ExecPlan: AIDE-BUILD-WORKER-RUN-SCHEMA-01

## Objective

Implement the minimal WorkerRun data contract as a protocol-shaped schema slice.

## Scope

- Add `core/protocol/worker_run.py` as metadata-only helper logic.
- Add `.aide/protocol/aide-worker-run.schema.json`.
- Add `worker-run status`, `worker-run project --source accepted-artifacts`, and `worker-run validate` CLI dispatch.
- Project accepted WorkUnit-related report artifacts into additive WorkerRun records.
- Write validation, future-work, unfinished-work, and queue evidence.

## Non-Goals

No worker execution, WorkUnit claim/run/finish/repair, worker leases, scheduler, supervisor, TestJob, Test Broker, Service, Commander, provider adapters, branch/worktree automation, target apply, active apply, rollback execution, release, promotion, network, Gateway, GitHub, or model/provider calls.

## Verification

Run focused WorkerRun tests, related predecessor tests, schema parsing, CLI validation, AIDE validation, and commit policy checks.

## Stop State

End at `needs_review`; next task is `AIDE-CHECK-WORKER-RUN-SCHEMA-01`.
