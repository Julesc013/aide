# Validation Commands

Planned and executed validation for this build:

```powershell
git status --short --branch
git diff --check
git diff --cached --check
py -3 -m py_compile core\interop\dominium\workunit_validation.py .aide\scripts\aide_lite.py .aide\scripts\tests\test_aide_dominium_workunit_validation_slice.py
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_dominium_workunit_validation_slice.py
py -3 .aide/scripts/aide_lite.py dominium-workunit-validation status
py -3 .aide/scripts/aide_lite.py dominium-workunit-validation run
py -3 .aide/scripts/aide_lite.py dominium-workunit-validation validate
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01
py -3 .aide/scripts/aide_lite.py workunit inspect --task-id AIDE-BUILD-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01
py -3 .aide/scripts/aide_lite.py validate
py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_dominium_readonly_seam*.py"
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_dominium_readonly_seam_repair_04.py
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_dominium_readonly_seam_repair_05.py
```

Focused pre-materialization checks also ran successfully:

```powershell
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_dominium_workunit_validation_slice.py
py -3 -m py_compile core\interop\dominium\workunit_validation.py .aide\scripts\aide_lite.py .aide\scripts\tests\test_aide_dominium_workunit_validation_slice.py
```
