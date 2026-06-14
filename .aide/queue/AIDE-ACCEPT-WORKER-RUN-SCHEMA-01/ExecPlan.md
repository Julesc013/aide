# ExecPlan: AIDE-ACCEPT-WORKER-RUN-SCHEMA-01

## Objective

Perform a check-only acceptance review for the completed `minimal_worker_run_schema` chain.

## Scope

- Review `AIDE-BUILD-WORKER-RUN-SCHEMA-01` and `AIDE-CHECK-WORKER-RUN-SCHEMA-01`.
- Decide whether the metadata-only WorkerRun schema/helper/projection/validation capability is admitted with warnings.
- Record evidence under this task and reports under `.aide/reports/worker-run-accept/`.
- Keep the queue index in sync with the acceptance review packet.

## Non-Goals

No WorkerRun repair or hardening, WorkerRun implementation edits, schema edits, test edits, TestJob implementation, worker execution, WorkUnit claim/run/finish/repair, leases, scheduler, supervisor, Test Broker, Service, Commander, provider adapters, branch/worktree automation, target apply, active apply, rollback execution, release, promotion, Gateway, network, GitHub, or model/provider calls.

## Verification Intent

Use task inspect/evidence, WorkerRun status/project/validate, focused WorkerRun tests, structural JSON/YAML parsing, overclaim/secret scans over changed files, `git diff --check`, and commit policy validation.

## Stop State

End at `needs_review`; next task is `AIDE-BUILD-TESTJOB-SCHEMA-01`.
