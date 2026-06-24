# Validation Commands

Commands run for this check:

```text
py -3 .aide/queue/AIDE-CHECK-EXECUTION-HOST-CONTRACT-V0-01/evidence/check_execution_host_contract.py
py -3 .aide/scripts/aide_lite.py execution-host status
py -3 .aide/scripts/aide_lite.py execution-host project --source contract-projection
py -3 .aide/scripts/aide_lite.py execution-host validate
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_execution_host_contract.py
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-EXECUTION-HOST-CONTRACT-V0-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-EXECUTION-HOST-CONTRACT-V0-01
py -3 .aide/scripts/aide_lite.py validate
Get-ChildItem .aide/queue/AIDE-CHECK-EXECUTION-HOST-CONTRACT-V0-01,.aide/reports/execution-host-contract-check -Recurse -File | Where-Object { $_.Name -ne 'check_execution_host_contract.py' } | Select-String -Pattern "<local path patterns>"
Get-ChildItem .aide/queue/AIDE-CHECK-EXECUTION-HOST-CONTRACT-V0-01,.aide/reports/execution-host-contract-check -Recurse -File | Where-Object { $_.Name -ne 'check_execution_host_contract.py' } | Select-String -Pattern "<secret-like patterns>"
git diff --check
git diff --cached --check
py -3 .aide/scripts/aide_lite.py commit check --latest
```
