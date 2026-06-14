# AIDE-CHECK-WORKUNIT-CLI-MUTATION-01 ExecPlan

## Objective

Independently check the WorkUnit queue metadata mutation CLI built by `AIDE-BUILD-WORKUNIT-CLI-MUTATION-01`.

## Scope

- Review `workunit create`, `workunit block`, and `workunit evidence add`.
- Verify dry-run and controlled apply behavior.
- Verify queue-local mutation, path safety, report truthfulness, compatibility, and forbidden-operation preservation.
- Write check evidence under this task and reports under `.aide/reports/workunit-cli-mutation-check/`.

## Non-Scope

No implementation changes. Do not build claim/run/finish/repair, runtime, leases, scheduler, WorkerRun, TestJob, Test Broker, Service, Commander, providers, branch/worktree automation, target apply, active apply, rollback, release, promotion, network, Gateway, GitHub, or model/provider calls.

## Validation

Run focused static review, CLI behavior checks, temp-root apply checks, compatibility commands, overclaim/secret scans, and task evidence validation.

## Stop State

Stop at `needs_review` with PASS, PASS_WITH_WARNINGS, FAILED_VALIDATION, BLOCKED, or PARTIAL.
