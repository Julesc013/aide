# WorkerRun Schema Check Report

- status: PASS_WITH_WARNINGS
- task_id: AIDE-CHECK-WORKER-RUN-SCHEMA-01
- checked_task_id: AIDE-BUILD-WORKER-RUN-SCHEMA-01
- checked_commit: 904866a14a2b1655cb78743a55afbf18f843d091
- decision: core behavior is safe; warnings are non-blocking.

## Summary

WorkerRun helper/schema/projection/validation slice is coherent, additive, source-traceable, compatible with accepted predecessors, and does not implement worker execution, claim, lease, scheduler, provider, TestJob/Test Broker, Service, Commander, branch/worktree, apply, rollback, release, network, Gateway, GitHub, or model/provider behavior.

## Warnings

- WorkerRun schema validation uses the accepted minimal local JSON Schema subset rather than full Draft 2020-12 enforcement. Blocking: false.
- Latest task packet remains stale and points at lifecycle fixture runner. Blocking: false.
- Validation/preflight commands refreshed out-of-scope generated reports; the churn was restored. Blocking: false.
- Initial negative probe and initial check-artifact scan had harness/scope issues and were corrected by reruns. Blocking: false.

## Projections

- .aide/reports/worker-run/projections/workunit-cli-mutation-acceptance.worker-run.json: source=.aide/reports/workunit-cli-mutation-acceptance/acceptance-report.json; provider=metadata_only; adapter=validation_observation; mode=validation_observation; traceability=PASS.
- .aide/reports/worker-run/projections/workunit-cli-mutation-check.worker-run.json: source=.aide/reports/workunit-cli-mutation-check/check-report.json; provider=metadata_only; adapter=validation_observation; mode=validation_observation; traceability=PASS.
- .aide/reports/worker-run/projections/workunit-cli-mutation-validation.worker-run.json: source=.aide/reports/workunit-cli-mutation/validation.json; provider=metadata_only; adapter=validation_observation; mode=validation_observation; traceability=PASS.
- .aide/reports/worker-run/projections/workunit-cli-validation.worker-run.json: source=.aide/reports/workunit-cli/validation.json; provider=metadata_only; adapter=validation_observation; mode=validation_observation; traceability=PASS.
- .aide/reports/worker-run/projections/workunit-queue-validation.worker-run.json: source=.aide/reports/workunit-queue/validation.json; provider=metadata_only; adapter=validation_observation; mode=validation_observation; traceability=PASS.

## Tests

- PASS: `py_compile protocol helpers and aide_lite` (PASS).
- PASS: `json.tool aide-worker-run.schema.json` (PASS).
- PASS: `unittest test_aide_worker_run_schema.py` (23 tests).
- PASS: `related unittest suites` (9+10+28+35+29+17+37 tests).

## Recommendation

- AIDE-ACCEPT-WORKER-RUN-SCHEMA-01
