# Validation Commands

Core validation:

```text
git status --short --branch
git diff --check
git diff --cached --check
git rev-parse 270b97d
git show --no-patch --format=fuller 270b97d
py -3 -m compileall core/interop/dominium core/protocol .aide/scripts/tests
py -3 .aide/queue/AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-04/evidence/tools/check_repair_04.py
py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_dominium_readonly_seam*.py"
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
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-04
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-04
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-04
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-04
py -3 .aide/scripts/aide_lite.py validate
rg -n --hidden --glob '!**/__pycache__/**' --glob '!**/*.pyc' "(BEGIN [A-Z ]*PRIVATE KEY|AKIA[0-9A-Z]{16}|sk-[A-Za-z0-9]{20,}|xox[baprs]-[A-Za-z0-9-]{20,}|ghp_[A-Za-z0-9_]{20,}|AIza[0-9A-Za-z_-]{20,}|password\s*[:=]|secret\s*[:=]|api[_-]?key\s*[:=]|token\s*[:=])" .aide/queue/AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-04 .aide/reports/dominium-readonly-seam-v0-repair-04-check
py -3 .aide/scripts/aide_lite.py commit check --latest
```

Final validation commands are recorded in `validation-results.md` after task metadata is finalized.
