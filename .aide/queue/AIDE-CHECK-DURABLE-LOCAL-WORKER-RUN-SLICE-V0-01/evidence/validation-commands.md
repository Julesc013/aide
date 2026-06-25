# Validation Commands

- `py -3 .aide/queue/AIDE-CHECK-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01/evidence/independent_check.py`
- `py -3 -m compileall .aide/queue/AIDE-CHECK-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01/evidence/independent_check.py`
- `py -3 .aide/scripts/aide_lite.py durable-worker-run status`
- `py -3 .aide/scripts/aide_lite.py durable-worker-run validate`
- `py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_durable_worker_run_slice.py"`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01`
- `py -3 .aide/scripts/aide_lite.py validate`
- `git diff --check`
- `git diff --cached --check`
- scoped absolute path and secret-like scan over check reports and evidence
