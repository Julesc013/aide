# Changed Files

## Source

- `core/protocol/worker_run.py`: minimal WorkerRun helper, validator, schema subset validation, additive projection, status/project/validate reports, and explicit non-capability boundaries.
- `core/protocol/__init__.py`: exports `worker_run`.
- `.aide/protocol/aide-worker-run.schema.json`: minimal WorkerRun JSON schema.
- `.aide/scripts/aide_lite.py`: CLI dispatch only for `worker-run status`, `worker-run project --source accepted-artifacts`, and `worker-run validate`.
- `.aide/scripts/tests/test_aide_worker_run_schema.py`: focused WorkerRun schema/projection/CLI tests.

## Queue And Evidence

- `.aide/queue/AIDE-BUILD-WORKER-RUN-SCHEMA-01/**`: task packet, status, prompt, ExecPlan, and evidence.
- `.aide/queue/index.yaml`: queue index entry for this task.

## Generated Reports

- `.aide/reports/worker-run/status.md`
- `.aide/reports/worker-run/projection-report.json`
- `.aide/reports/worker-run/projection-report.md`
- `.aide/reports/worker-run/validation.json`
- `.aide/reports/worker-run/validation.md`
- `.aide/reports/worker-run/future-work.md`
- `.aide/reports/worker-run/unfinished-work.md`
- `.aide/reports/worker-run/projections/*.worker-run.json`

Unrelated generated churn from predecessor validation commands was restored.
