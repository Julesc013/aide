# Validation Commands

Commands for this acceptance gate:

```text
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-EXECUTION-HOST-CONTRACT-V0-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-EXECUTION-HOST-CONTRACT-V0-01
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-EXECUTION-HOST-CONTRACT-V0-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-EXECUTION-HOST-CONTRACT-V0-01
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-ACCEPT-EXECUTION-HOST-CONTRACT-V0-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-ACCEPT-EXECUTION-HOST-CONTRACT-V0-01
py -3 .aide/scripts/aide_lite.py execution-host validate
py -3 .aide/scripts/aide_lite.py validate
Get-ChildItem .aide/queue/AIDE-ACCEPT-EXECUTION-HOST-CONTRACT-V0-01,.aide/reports/execution-host-contract-accept -Recurse -File | Select-String -Pattern "<local path patterns>"
Get-ChildItem .aide/queue/AIDE-ACCEPT-EXECUTION-HOST-CONTRACT-V0-01,.aide/reports/execution-host-contract-accept -Recurse -File | Select-String -Pattern "<secret-like patterns>"
git diff --check
git diff --cached --check
py -3 .aide/scripts/aide_lite.py commit check --latest
```
