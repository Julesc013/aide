# TestJob Acceptance Report

- task_id: `AIDE-ACCEPT-TESTJOB-SCHEMA-01`
- result: `ACCEPTED_WITH_WARNINGS`
- accepted_capability: `minimal_test_job_schema`
- predecessor: `AIDE-ACCEPT-WORKER-RUN-SCHEMA-01`
- build_task: `AIDE-BUILD-TESTJOB-SCHEMA-01`
- check_task: `AIDE-CHECK-TESTJOB-SCHEMA-01`
- recommended_next_task: `AIDE-BUILD-REFERENCE-ID-SCHEME-01`

## Accepted Scope

- metadata-only TestJob schema
- TestJob helper/projection/validation
- `test-job status/project/validate` CLI dispatch
- additive accepted-artifact projections

## Result

Accepted with warnings. The warnings are non-blocking because the build and independent check evidence show the minimal TestJob schema slice passes focused tests, CLI validation, predecessor compatibility checks, projection checks, fail-closed unsupported command checks, and overclaiming scans.

## Non-Capability Boundary

This acceptance does not authorize Test Broker runtime, async test execution, test job submission/run/retry/summarize runtime, worker execution, WorkUnit claim/run/finish/repair, leases, scheduler, supervisor, Service, Commander, provider adapters, branch/worktree automation, target apply, active apply, rollback execution, release, promotion, Gateway, network, GitHub mutation, model/provider calls, production readiness, release readiness, or broad autonomous runtime behavior.
