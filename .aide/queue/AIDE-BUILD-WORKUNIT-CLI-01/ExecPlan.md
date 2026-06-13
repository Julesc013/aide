# ExecPlan: AIDE-BUILD-WORKUNIT-CLI-01

## Objective

Build the first read-only `workunit` CLI surface over accepted WorkUnit Queue V1 objects.

## Scope

- Add `core/protocol/workunit_cli.py` for read-only command helpers and reports.
- Keep `.aide/scripts/aide_lite.py` as dispatch only.
- Add `workunit status`, `workunit list`, `workunit inspect --task-id`, and `workunit validate`.
- Add focused tests and additive reports under `.aide/reports/workunit-cli/`.

## Boundaries

- No `workunit create`, `claim`, `run`, `block`, `finish`, or `repair`.
- No runtime scheduler, supervisor, WorkerRun, TestJob, Test Broker, Service, Commander, provider adapter, branch/worktree automation, target repo apply, active repo apply, rollback execution, release, promotion, Gateway, network, GitHub, or model/provider calls.
- No destructive migration of queue tasks or accepted reports.

## Verification

Run py_compile, focused WorkUnit CLI tests, predecessor protocol tests, lifecycle/apply smoke checks, read-only CLI commands, negative unsupported-command checks, report parsing, secret/overclaim scans, `aide_lite.py validate`, `aide_lite.py test`, `git diff --check`, and commit-policy checks.

## Stop State

Stop at `needs_review`.
