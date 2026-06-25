# Validation Results

Validation completed so far:

- `py -3 .aide/scripts/aide_lite.py durable-worker-run fixture`: PASS_WITH_WARNINGS.
- event-record consistency probe: PASS; fixture `host_result=PASS`, EventRecord payload `result=PASS`, EventRecord status `result=PASS`.
- `py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_durable_worker_run_slice.py"`: PASS, 4 tests.
- `py -3 .aide/scripts/aide_lite.py durable-worker-run validate`: PASS_WITH_WARNINGS, validated true, error count 0.
- `py -3 -m compileall core/service/durable_worker_run.py .aide/scripts/tests/test_aide_durable_worker_run_slice.py`: PASS.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-REPAIR-01`: PASS, complete, missing evidence 0.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-REPAIR-01`: PASS, no missing evidence.
- `py -3 .aide/scripts/aide_lite.py durable-worker-run status`: PASS_WITH_WARNINGS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `git diff --check`: PASS.
- `git diff --cached --check`: PASS.
- Scoped absolute path and secret-like scan over repair reports and task evidence: PASS, no hits.

Final task inspect, task evidence, broad validation, diff checks, leak scan, and commit-policy results are added before commit.
