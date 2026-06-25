# Validation Commands

```text
py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_local_process_execution_host.py"
py -3 .aide/scripts/aide_lite.py local-process-execution-host run
py -3 .aide/scripts/aide_lite.py local-process-execution-host validate
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-02
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-02
py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_registered_process*.py"
py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_execution_host*.py"
py -3 -m compileall core/execution .aide/scripts/tests
py -3 .aide/scripts/aide_lite.py validate
git diff --check
absolute local path scan over task evidence and local-process reports
secret-like scan over task evidence and local-process reports
```
