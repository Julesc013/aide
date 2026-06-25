# Validation Results

Initial independent harness result:

- `REQUEST_CHANGES`
- `material_finding_count: 1`
- `missing_evidence: 0`
- `recommended_next_task: AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-REPAIR-01`

Runtime observations that passed:

- Fresh fixture process call count was exactly `1`.
- Authorization result was `allowed`.
- Trust grant was consumed.
- Service event sequence was `[1, 2, 3, 4, 5, 6]`.
- SQLite state contained expected object, event, idempotency, and artifact metadata rows.
- Idempotent replay did not launch a second host run.
- Raw event stream and worker artifact digests matched declared hashes.
- Explicit false-boundary fields remained boolean `false`.

The remaining material defect is the EventRecord payload result mismatch described in `material-findings.md`.

Additional validation completed after task finalization:

- `py -3 -m compileall .aide/queue/AIDE-CHECK-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01/evidence/independent_check.py`: PASS.
- `py -3 .aide/scripts/aide_lite.py durable-worker-run status`: PASS_WITH_WARNINGS.
- `py -3 .aide/scripts/aide_lite.py durable-worker-run validate`: PASS_WITH_WARNINGS.
- `py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_durable_worker_run_slice.py"`: PASS, 4 tests.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01`: PASS, complete, missing evidence 0.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01`: PASS, no missing evidence.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `git diff --check`: PASS.
- `git diff --cached --check`: PASS.
- Scoped absolute path and secret-like scan over check reports and task evidence: PASS, no hits.
