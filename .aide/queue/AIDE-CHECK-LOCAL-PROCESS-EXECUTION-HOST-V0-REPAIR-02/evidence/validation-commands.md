# Validation Commands

```text
py -3 .aide/queue/AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-02/evidence/check_local_process_host_repair_02.py
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-02
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-02
py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_local_process_execution_host.py"
py -3 .aide/scripts/aide_lite.py validate
git diff --check
absolute local path scan over check task evidence and reports
secret-like scan over check task evidence and reports
```
