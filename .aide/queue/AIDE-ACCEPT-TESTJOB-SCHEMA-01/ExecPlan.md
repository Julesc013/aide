# ExecPlan: AIDE-ACCEPT-TESTJOB-SCHEMA-01

## Objective

Accept or reject the `minimal_test_job_schema` protocol slice using live queue evidence from `AIDE-BUILD-TESTJOB-SCHEMA-01` and `AIDE-CHECK-TESTJOB-SCHEMA-01`.

## Scope

- Review the build task, check task, predecessor WorkerRun acceptance, TestJob reports, and validation evidence.
- Produce task-local acceptance evidence.
- Produce `.aide/reports/test-job-accept/*` acceptance reports.
- Update `.aide/queue/index.yaml`, `PLANS.md`, and `IMPLEMENT.md`.
- Stop at `needs_review`.

## Non-Goals

No implementation repair, Test Broker runtime, async test execution, test job submission/run/retry/summarize runtime, worker execution, WorkUnit claim/run/finish/repair, leases, scheduler, supervisor, Service, Commander, provider adapters, branch/worktree automation, target apply, active apply, rollback execution, release, promotion, network, Gateway, GitHub mutation, or model/provider calls.

## Current Facts

- `AIDE-ACCEPT-WORKER-RUN-SCHEMA-01` accepted `minimal_worker_run_schema` with warnings.
- `AIDE-BUILD-TESTJOB-SCHEMA-01` is `needs_review` with result `PASS`.
- `AIDE-CHECK-TESTJOB-SCHEMA-01` is `needs_review` with result `PASS_WITH_WARNINGS`.
- `.aide/context/latest-task-packet.md` is stale relative to live queue truth and is not execution authority.
- The next post-acceptance task is `AIDE-BUILD-REFERENCE-ID-SCHEME-01`, not PatchTransaction.

## Progress

- [x] Verified live queue state and predecessor evidence availability.
- [x] Reviewed build evidence and generated TestJob reports.
- [x] Reviewed independent check evidence and warnings.
- [x] Wrote acceptance evidence and acceptance reports.
- [x] Recorded the review in queue index and root planning/execution logs.
- [x] Run final validation and contain generated report churn.
- [x] Prepare the commit-ready change set.

## Validation Intent

Run task inspect/evidence for this acceptance task, JSON validation for the acceptance report, TestJob status/validate, predecessor protocol validations, repository validation, and whitespace checks. Restore any out-of-scope generated report churn before committing.

## Evidence

Task evidence lives under `.aide/queue/AIDE-ACCEPT-TESTJOB-SCHEMA-01/evidence/`.

## Recovery

If interrupted, re-run the validation commands in `evidence/test-and-validation-review.md`, confirm no out-of-scope generated reports remain dirty, and update `status.yaml` if validation results changed. Do not edit implementation files in this acceptance task.

## Stop State

End at `needs_review` with result `ACCEPTED_WITH_WARNINGS`.
