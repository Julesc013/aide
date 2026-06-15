# AIDE-BUILD-TESTJOB-SCHEMA-01

Build a minimal, envelope-backed, metadata-only TestJob schema/helper/projection/validation slice after accepted WorkerRun.

Allowed implementation surface:

- `.aide/protocol/aide-test-job.schema.json`
- `core/protocol/test_job.py`
- `core/protocol/__init__.py`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_test_job_schema.py`
- `.aide/reports/test-job/**`
- `.aide/queue/AIDE-BUILD-TESTJOB-SCHEMA-01/**`
- `.aide/queue/index.yaml`
- root planning/execution/documentation indexes

Required CLI:

- `test-job status`
- `test-job project --source accepted-artifacts`
- `test-job validate`

Hard boundary:

- No Test Broker runtime.
- No async execution.
- No test-job submit/run/retry/summarize runtime.
- No worker execution.
- No WorkUnit claim/run/finish/repair.
- No scheduler, leases, supervisor, Service, Commander, providers, Gateway, network, GitHub mutation, branch/worktree automation, target apply, active apply, rollback execution, release, promotion, or model/provider calls.

Stop at `needs_review` and recommend `AIDE-CHECK-TESTJOB-SCHEMA-01`.
