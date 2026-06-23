# Validation Commands

Commands planned or run for this check:

```text
git status --short --branch
py -3 -m py_compile .aide\queue\AIDE-CHECK-DOMINIUM-REGISTERED-VALIDATION-BACKEND-RELABEL-01\evidence\independent_relabel_check.py
py -3 .aide\queue\AIDE-CHECK-DOMINIUM-REGISTERED-VALIDATION-BACKEND-RELABEL-01\evidence\independent_relabel_check.py
py -3 -m py_compile core\interop\dominium\registered_validation_backend.py .aide\scripts\aide_lite.py .aide\scripts\tests\test_aide_dominium_registered_validation_backend.py
py -3 .aide\scripts\tests\test_aide_dominium_registered_validation_backend.py
py -3 .aide\scripts\aide_lite.py dominium-registered-validation validate
py -3 .aide\scripts\aide_lite.py task inspect --task-id AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-RELABEL-01
py -3 .aide\scripts\aide_lite.py task evidence --task-id AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-RELABEL-01
py -3 .aide\scripts\aide_lite.py task inspect --task-id AIDE-CHECK-DOMINIUM-REGISTERED-VALIDATION-BACKEND-RELABEL-01
py -3 .aide\scripts\aide_lite.py task evidence --task-id AIDE-CHECK-DOMINIUM-REGISTERED-VALIDATION-BACKEND-RELABEL-01
git -C <dominium-root> status --short --branch
strict local-absolute-path scan over check outputs
strict secret-like token scan over check outputs
py -3 .aide\scripts\aide_lite.py validate
git diff --check
git diff --cached --check
py -3 .aide\scripts\aide_lite.py commit check --latest
```
