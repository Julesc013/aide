# Validation Commands

```text
py -3 -m py_compile core\interop\dominium\registered_validation_backend.py .aide\scripts\tests\test_aide_dominium_registered_validation_backend.py .aide\scripts\aide_lite.py
py -3 -m unittest discover -s .aide\scripts\tests -p "test_aide_dominium_registered_validation_backend.py"
py -3 .aide\scripts\aide_lite.py dominium-registered-validation run
py -3 .aide\scripts\aide_lite.py dominium-registered-validation validate
strict local-path and secret-like scan for task/report surfaces
git -C <dominium-root> status --short --branch
git diff --check
git diff --cached --check
py -3 -m compileall core\interop\dominium core\protocol .aide\scripts\tests
py -3 .aide\scripts\aide_lite.py validate
```
