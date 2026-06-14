# WorkerRun Schema Acceptance Report

- task_id: AIDE-ACCEPT-WORKER-RUN-SCHEMA-01
- result: ACCEPTED_WITH_WARNINGS
- accepted_capability: minimal_worker_run_schema
- recommended_next_task: AIDE-BUILD-TESTJOB-SCHEMA-01

## Summary

The metadata-only WorkerRun schema slice is accepted as an AIDE protocol capability with warnings. The accepted scope is the WorkerRun envelope-backed object shape, helper/projection/validation behavior, additive accepted-artifact projections, and `worker-run status/project/validate` CLI dispatch.

## Source Chain

- AIDE-BUILD-WORKER-RUN-SCHEMA-01: PASS, implementation completed, stopped at needs_review.
- AIDE-CHECK-WORKER-RUN-SCHEMA-01: PASS_WITH_WARNINGS, check completed, stopped at needs_review.

## Warnings

- Full Draft 2020-12 JSON Schema validation remains deferred; non-blocking.
- WorkerRun remains metadata-only by design; non-blocking.
- `.aide/context/latest-task-packet.md` is stale relative to queue truth; non-blocking.
- Prior check harness probe issues were corrected by reruns; non-blocking.
- Generated report churn must continue to be contained; non-blocking.

## Boundary

This acceptance does not authorize worker execution, WorkUnit claim/run/finish/repair, leases, scheduler, supervisor, TestJob, Test Broker, Service, Commander, provider adapters, branch/worktree automation, target apply, active apply, rollback execution, uninstall execution, release, promotion, Gateway, network, GitHub mutation, model/provider calls, production readiness, release readiness, or broad autonomous runtime behavior.
