# Validation Commands

Commands planned or run for this check:

```text
git status --short --branch
py -3 -m py_compile .aide\queue\AIDE-CHECK-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01\evidence\independent_backend_check.py
py -3 .aide\queue\AIDE-CHECK-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01\evidence\independent_backend_check.py
py -3 .aide\scripts\aide_lite.py task inspect --task-id AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01
py -3 .aide\scripts\aide_lite.py task evidence --task-id AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01
py -3 .aide\scripts\aide_lite.py task inspect --task-id AIDE-CHECK-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01
py -3 .aide\scripts\aide_lite.py task evidence --task-id AIDE-CHECK-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01
git -C <dominium-root> status --short --branch
strict local-absolute-path scan over check task/report outputs
strict secret-like token scan over check task/report outputs
git diff --check
git diff --cached --check
py -3 .aide\scripts\aide_lite.py validate
py -3 .aide\scripts\aide_lite.py commit check --latest
```
