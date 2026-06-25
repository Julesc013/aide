# Validation Commands

Commands run or scheduled for this build:

```powershell
git status --short --branch --untracked-files=all
py -3 -m py_compile core\protocol\distribution_manifest.py .aide\scripts\aide_lite.py
py -3 .aide\scripts\tests\test_aide_distribution_manifest_v1.py
py -3 .aide\scripts\aide_lite.py distribution-manifest status
py -3 .aide\scripts\aide_lite.py distribution-manifest project
py -3 .aide\scripts\aide_lite.py distribution-manifest validate
py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_distribution_manifest_v1.py"
py -3 .aide\scripts\aide_lite.py task inspect --task-id AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-01
py -3 .aide\scripts\aide_lite.py task evidence --task-id AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-01
py -3 .aide\scripts\aide_lite.py validate
git diff --check
git diff --cached --check
py -3 .aide\scripts\aide_lite.py commit check --latest
```
