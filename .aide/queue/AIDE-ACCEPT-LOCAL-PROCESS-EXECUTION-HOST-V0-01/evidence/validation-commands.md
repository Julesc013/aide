# Validation Commands

Planned and executed validation:

```text
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-02
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-02
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-02
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-02
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-ACCEPT-LOCAL-PROCESS-EXECUTION-HOST-V0-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-ACCEPT-LOCAL-PROCESS-EXECUTION-HOST-V0-01
py -3 .aide/scripts/aide_lite.py local-process-execution-host validate
py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_local_process_execution_host.py"
py -3 .aide/scripts/aide_lite.py validate
git diff --check
git diff --cached --check
acceptance report/evidence absolute-path scan
acceptance report/evidence secret-like scan
py -3 .aide/scripts/aide_lite.py commit check --latest
```
