# ExecPlan: AIDE-CHECK-TESTJOB-SCHEMA-01

## Objective

Independently verify the `minimal_test_job_schema` slice from `AIDE-BUILD-TESTJOB-SCHEMA-01`.

## Scope

- Review the TestJob helper, schema, CLI dispatch, tests, projections, reports, and build evidence.
- Verify compatibility with accepted contract envelope, EvidencePacket, WorkUnit Queue, WorkUnit CLI, WorkerRun, and WorkerRun acceptance layers.
- Run focused structural checks, focused TestJob tests, CLI validation, fail-closed command checks, boundary scans, and whitespace checks.
- Produce check evidence and `.aide/reports/test-job-check/check-report.*`.

## Allowed Paths

- `.aide/queue/AIDE-CHECK-TESTJOB-SCHEMA-01/**`
- `.aide/reports/test-job-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

## Non-Goals

No implementation repair, Test Broker runtime, async test execution, test job submission/run/retry/summarize runtime, worker execution, WorkUnit claim/run/finish/repair, leases, scheduler, supervisor, Service, Commander, provider adapters, branch/worktree automation, target apply, active apply, rollback execution, release, promotion, network, Gateway, GitHub, or model/provider calls.

## Current Facts

- `AIDE-BUILD-TESTJOB-SCHEMA-01` exists, is indexed, and is at `needs_review` with result `PASS`.
- The build task recommends `AIDE-CHECK-TESTJOB-SCHEMA-01`.
- The user-supplied frozen sequence for this turn places `AIDE-ACCEPT-TESTJOB-SCHEMA-01` next, then `AIDE-BUILD-REFERENCE-ID-SCHEME-01`.
- `.aide/context/latest-task-packet.md` is stale relative to live queue truth and was not used as execution authority.

## Progress

- [x] Read queue policy, source-of-truth references, build task evidence, and neighboring check patterns.
- [x] Ran focused structural checks and TestJob tests.
- [x] Ran TestJob CLI status/project/validate and predecessor validations.
- [x] Verified unsupported execution subcommands fail closed.
- [x] Ran corrected secret and overclaim scans.
- [x] Restored out-of-scope generated report churn before creating check artifacts.
- [x] Wrote check report and task-local evidence.

## Validation

Validation is recorded in `evidence/validation.md` and `.aide/reports/test-job-check/check-report.json`.

## Evidence

Task evidence lives under `.aide/queue/AIDE-CHECK-TESTJOB-SCHEMA-01/evidence/`.

## Recovery

If interrupted, rerun the commands listed in `evidence/validation.md`, confirm no out-of-scope generated report churn remains, then update `status.yaml` and the check report. Do not edit TestJob implementation files in this check task.

## Stop State

End at `needs_review` with result `PASS_WITH_WARNINGS`.
