# Validation Commands

```text
py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_trust_authorization_contract.py"
py -3 .aide/scripts/aide_lite.py trust status
py -3 .aide/scripts/aide_lite.py trust project --source contract-projection
py -3 .aide/scripts/aide_lite.py trust validate
py -3 -m compileall core/protocol .aide/scripts/tests
py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_registered_process_execution_provider.py"
py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_execution_host_contract.py"
py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_local_process_execution_host.py"
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01
py -3 .aide/scripts/aide_lite.py validate
git diff --check
git diff --cached --check
trust contract local-path scan
trust contract secret-like scan
py -3 .aide/scripts/aide_lite.py commit check --latest
```
