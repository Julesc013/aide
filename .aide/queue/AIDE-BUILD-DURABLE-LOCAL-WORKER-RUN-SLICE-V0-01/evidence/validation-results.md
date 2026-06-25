# Validation Results

All validation commands passed unless noted otherwise:

- `py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_durable_worker_run_slice.py"`: PASS, 4 tests.
- `py -3 -m compileall core/service/durable_worker_run.py .aide/scripts/tests/test_aide_durable_worker_run_slice.py .aide/scripts/aide_lite.py`: PASS.
- `py -3 .aide/scripts/aide_lite.py durable-worker-run fixture`: PASS_WITH_WARNINGS, `process_call_count: 1`.
- `py -3 .aide/scripts/aide_lite.py durable-worker-run validate`: PASS_WITH_WARNINGS, validated true, error_count 0.
- `py -3 .aide/scripts/aide_lite.py durable-worker-run status`: PASS_WITH_WARNINGS.
- `py -3 .aide/scripts/aide_lite.py local-trust validate`: PASS_WITH_WARNINGS, validated true.
- `py -3 .aide/scripts/aide_lite.py local-service validate`: PASS_WITH_WARNINGS, validated true.
- `py -3 .aide/scripts/aide_lite.py local-process-execution-host validate`: PASS_WITH_WARNINGS, validated true.
- `py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_local_trust_enforcement.py"`: PASS, 6 tests.
- `py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_local_service_foundation.py"`: PASS, 7 tests.
- `py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_local_process_execution_host.py"`: PASS, 9 tests.
- `py -3 -m compileall core/service core/execution core/protocol .aide/scripts/tests`: PASS.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01`: PASS, complete, missing_evidence 0.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01`: PASS, no missing evidence.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `git diff --check`: PASS.
- `git diff --cached --check`: PASS.
- Scoped absolute path and secret-like scan over durable reports and task evidence: PASS, no hits.
