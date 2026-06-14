# AIDE-ACCEPT-WORKER-RUN-SCHEMA-01

Perform acceptance review for the completed metadata-only WorkerRun schema chain:

- `AIDE-BUILD-WORKER-RUN-SCHEMA-01`
- `AIDE-CHECK-WORKER-RUN-SCHEMA-01`

Accept only the `minimal_worker_run_schema` capability if the build/check evidence supports it. The accepted scope is the envelope-backed WorkerRun object, schema/helper/projection/validation behavior, metadata-only accepted-artifact projections, and `worker-run status/project/validate` CLI dispatch.

Do not build, repair, or harden WorkerRun in this task. Do not implement TestJob, Test Broker, worker execution, WorkUnit claim/run/finish/repair, leases, scheduler, provider adapters, Service, Commander, branch/worktree automation, target apply, active apply, rollback, release, promotion, Gateway, network, GitHub mutation, or model/provider calls.

Expected result if evidence matches live queue truth: `ACCEPTED_WITH_WARNINGS`, with `AIDE-BUILD-TESTJOB-SCHEMA-01` as the next task.
