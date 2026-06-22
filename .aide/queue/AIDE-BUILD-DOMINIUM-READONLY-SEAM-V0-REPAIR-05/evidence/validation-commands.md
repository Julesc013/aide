# Validation Commands

```text
git status --short --branch
git diff --check
git diff --cached --check
py -3 -m compileall core/interop/dominium core/protocol .aide/scripts/tests
py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_dominium_readonly_seam_repair_05.py"
py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_dominium_readonly_seam_repair_04.py"
py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_dominium_readonly_seam_repair_03.py"
py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_dominium_readonly_seam_repair_02.py"
py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_dominium_readonly_seam_repair.py"
py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_dominium_readonly_seam.py"
py -3 .aide/scripts/aide_lite.py dominium-seam status
py -3 .aide/scripts/aide_lite.py dominium-seam snapshot
py -3 .aide/scripts/aide_lite.py dominium-seam project
py -3 .aide/scripts/aide_lite.py dominium-seam validate
py -3 .aide/scripts/aide_lite.py dominium-seam diff
py -3 .aide/scripts/aide_lite.py dominium-seam demo
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-05
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-05
py -3 .aide/scripts/aide_lite.py validate
python-json-parse-scan over Repair 05 and regenerated seam JSON
python-secret-like-scan over Repair 05 and changed code/test surfaces
git -C C:\Projects\Dominium\dominium status --short --branch
py -3 .aide/scripts/aide_lite.py commit check --latest
```
