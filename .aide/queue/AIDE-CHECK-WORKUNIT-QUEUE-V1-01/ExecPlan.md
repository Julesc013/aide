# ExecPlan: AIDE-CHECK-WORKUNIT-QUEUE-V1-01

## Objective

Independently check the `AIDE-BUILD-WORKUNIT-QUEUE-V1-01` implementation and produce concrete evidence for pass, warning, failure, blocked, or partial classification.

## Scope

- Read and review the WorkUnit queue helper, schema, CLI dispatch, tests, reports, projections, and source queue task packets.
- Rerun focused validation and compatibility commands.
- Verify negative behavior using existing focused tests and helper behavior.
- Write check evidence and a concise check report.

## Boundaries

- No implementation code changes.
- No WorkUnit create/list/claim/block/finish/repair CLI.
- No runtime, scheduler, supervisor, TestJob, Test Broker, Service, Commander, provider adapter, branch/worktree, target apply, active apply, rollback, release, network, Gateway, GitHub, or model/provider behavior.

## Validation

Run focused unit tests, predecessor protocol tests, WorkUnit queue commands, predecessor validation commands, JSON parsing, secret and overclaim scans, `git diff --check`, and commit-policy validation after the check commit.

## Stop State

Stop at `needs_review`.
