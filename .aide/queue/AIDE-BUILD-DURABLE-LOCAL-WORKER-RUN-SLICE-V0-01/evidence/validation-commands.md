# Validation Commands

```text
py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_durable_worker_run_slice.py"
py -3 -m compileall core/service/durable_worker_run.py .aide/scripts/tests/test_aide_durable_worker_run_slice.py .aide/scripts/aide_lite.py
py -3 .aide/scripts/aide_lite.py durable-worker-run fixture
py -3 .aide/scripts/aide_lite.py durable-worker-run validate
py -3 .aide/scripts/aide_lite.py durable-worker-run status
py -3 .aide/scripts/aide_lite.py local-trust validate
py -3 .aide/scripts/aide_lite.py local-service validate
py -3 .aide/scripts/aide_lite.py local-process-execution-host validate
py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_local_trust_enforcement.py"
py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_local_service_foundation.py"
py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_local_process_execution_host.py"
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01
py -3 .aide/scripts/aide_lite.py validate
git diff --check
git diff --cached --check
py -3 .aide/scripts/aide_lite.py commit check --latest
```
