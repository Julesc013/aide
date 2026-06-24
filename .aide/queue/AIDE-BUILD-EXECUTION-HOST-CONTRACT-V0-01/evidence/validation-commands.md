# Validation Commands

Commands:

```text
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_execution_host_contract.py
py -3 .aide/scripts/aide_lite.py execution-host status
py -3 .aide/scripts/aide_lite.py execution-host project --source contract-projection
py -3 .aide/scripts/aide_lite.py execution-host validate
py -3 -m compileall core/protocol .aide/scripts/tests
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_registered_process_provider.py
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_worker_run_schema.py
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-EXECUTION-HOST-CONTRACT-V0-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-EXECUTION-HOST-CONTRACT-V0-01
py -3 .aide/scripts/aide_lite.py validate
local path and secret-like scans over new surfaces
git diff --check
git diff --cached --check
py -3 .aide/scripts/aide_lite.py commit check --latest
```
