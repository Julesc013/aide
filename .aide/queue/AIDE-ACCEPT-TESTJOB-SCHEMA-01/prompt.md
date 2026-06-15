# Queue Prompt: AIDE-ACCEPT-TESTJOB-SCHEMA-01

Perform a check-only acceptance review for `AIDE-BUILD-TESTJOB-SCHEMA-01` and `AIDE-CHECK-TESTJOB-SCHEMA-01`.

Expected result if live evidence matches the queue records: `ACCEPTED_WITH_WARNINGS`.

Accept only `minimal_test_job_schema`: metadata-only TestJob schema, helper/projection/validation behavior, additive accepted-artifact projections, and `test-job status/project/validate` CLI dispatch.

Do not implement or authorize Test Broker runtime, async test execution, test job submission/run/retry/summarize runtime, worker execution, WorkUnit claim/run/finish/repair, leases, scheduler, supervisor, Service, Commander, provider adapters, branch/worktree automation, target apply, active apply, rollback execution, release, promotion, GitHub mutation, Gateway, network calls, model/provider calls, production-ready claims, release-ready claims, or broad runtime behavior.

Use live `.aide/queue/` task files as canonical authority. The latest task packet may be stale.

Create acceptance task evidence and `.aide/reports/test-job-accept/*` reports. Stop at `needs_review`.

Recommended next task after acceptance: `AIDE-BUILD-REFERENCE-ID-SCHEME-01`. Do not recommend PatchTransaction next.
