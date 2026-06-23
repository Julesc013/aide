# Validation Commands

Executed:

```powershell
git status --short --branch
git diff --check
git diff --cached --check
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-ACCEPT-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-ACCEPT-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01
py -3 .aide/scripts/aide_lite.py validate
py -3 .aide/scripts/aide_lite.py commit check --latest
```

Also executed a strict secret-like and absolute-path scan over acceptance
reports and task evidence.
