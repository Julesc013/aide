# ExecPlan: AIDE-BUILD-WORKUNIT-QUEUE-V1-01

## Objective

Build the minimal WorkUnit queue v1 slice as a protocol-shaped projection and validation layer over existing filesystem queue tasks.

## Scope

- Add `core/protocol/workunit.py` as the bounded helper module.
- Add `.aide/protocol/aide-workunit.schema.json`.
- Add `workunit-queue status`, `project`, and `validate` CLI dispatch.
- Add focused unit tests and additive reports under `.aide/reports/workunit-queue/`.

## Boundaries

- No WorkUnit create/list/claim/block/finish/repair CLI.
- No runtime scheduler, supervisor, Test Broker, Service, Commander, provider adapter, branch/worktree automation, target repo apply, active repo apply, rollback execution, release, or promotion.
- No destructive migration of queue tasks or accepted reports.

## Validation

Run focused protocol tests, predecessor protocol tests, lifecycle/apply smoke checks, generated report validation, `aide_lite.py validate`, `aide_lite.py test`, `git diff --check`, and commit-policy checks before final handoff.

## Stop State

Stop at `needs_review`.
