# Validation Commands

Commands planned for this acceptance:

```text
py -3 .aide/scripts/aide_lite.py durable-worker-run validate
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-REPAIR-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-REPAIR-01
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-ACCEPT-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-ACCEPT-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01
py -3 .aide/scripts/aide_lite.py validate
git diff --check
git diff --cached --check
```
