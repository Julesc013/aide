# Validation Commands

- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_local_process_execution_host.py`
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_registered_process_provider.py`
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_execution_host_contract.py`
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_self_validation_process_adapter.py`
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_dominium_registered_validation_backend.py`
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_eureka_readonly_process_adapter.py`
- `py -3 .aide/scripts/aide_lite.py local-process-execution-host validate`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-01`
- `py -3 .aide/scripts/aide_lite.py validate`
- `git diff --check`
- `git diff --cached --check`
