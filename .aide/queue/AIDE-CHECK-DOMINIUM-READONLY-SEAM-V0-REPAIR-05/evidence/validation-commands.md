# Validation Commands

```text
git status --short --branch
py -3 .aide/queue/AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-05/evidence/independent_repair05_check.py
git diff --check
git diff --cached --check
py -3 -m compileall core/interop/dominium core/protocol .aide/scripts/tests
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-05
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-05
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-05
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-05
py -3 .aide/scripts/aide_lite.py validate
python-json-parse-scan over Repair 05 check JSON
python-secret-like-scan over Repair 05 check surfaces
git -C C:\Projects\Dominium\dominium status --short --branch
py -3 .aide/scripts/aide_lite.py commit check --latest
```
