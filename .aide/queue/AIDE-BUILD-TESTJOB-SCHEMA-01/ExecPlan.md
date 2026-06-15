# ExecPlan: AIDE-BUILD-TESTJOB-SCHEMA-01

## Objective

Build the minimal metadata-only `TestJob` protocol slice after the accepted `minimal_worker_run_schema` capability.

## Scope

- Add `.aide/protocol/aide-test-job.schema.json`.
- Add `core/protocol/test_job.py` for schema loading, helper validation, metadata-only projection, and report generation.
- Add thin `test-job status/project/validate` dispatch in `.aide/scripts/aide_lite.py`.
- Add focused TestJob tests.
- Write reports under `.aide/reports/test-job/`.
- Write task evidence and stop at `needs_review`.

## Non-Goals

No Test Broker runtime, async execution, queued test execution, scheduler, leases, supervisor, worker execution, WorkUnit claim/run/finish/repair, Service, Commander, provider adapters, branch/worktree automation, active repo apply, target apply, rollback execution, release, promotion, Gateway, network, GitHub mutation, or model/provider calls.

## Verification Intent

Use focused TestJob tests, schema JSON parsing, Python compile checks, `test-job status/project/validate`, predecessor protocol validation commands, task inspect/evidence, boundary scans, secret scans, `git diff --check`, and commit policy validation.

## Stop State

End at `needs_review`; recommended next task is `AIDE-CHECK-TESTJOB-SCHEMA-01`.
