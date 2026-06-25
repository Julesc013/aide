# Validation Commands

- `py -3 .aide/scripts/aide_lite.py durable-worker-run fixture`
- event-record consistency probe comparing fixture report `host_result` to EventRecord `spec.payload.result`
- `py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_durable_worker_run_slice.py"`
- `py -3 .aide/scripts/aide_lite.py durable-worker-run validate`
- `py -3 -m compileall core/service/durable_worker_run.py .aide/scripts/tests/test_aide_durable_worker_run_slice.py`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-REPAIR-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-REPAIR-01`
- `py -3 .aide/scripts/aide_lite.py validate`
- `git diff --check`
- `git diff --cached --check`
- scoped absolute path and secret-like scan over repair reports and task evidence
