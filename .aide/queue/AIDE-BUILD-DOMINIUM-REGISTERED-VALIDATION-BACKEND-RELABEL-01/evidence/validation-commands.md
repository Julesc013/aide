# Validation Commands

Commands planned or run for this task:

```text
git status --short --branch
py -3 .aide/scripts/aide_lite.py git plan
git -C <dominium-root> status --short --branch
py -3 -m py_compile core/interop/dominium/registered_validation_backend.py .aide/scripts/aide_lite.py .aide/scripts/tests/test_aide_dominium_registered_validation_backend.py
py -3 -m unittest .aide.scripts.tests.test_aide_dominium_registered_validation_backend
py -3 .aide/scripts/aide_lite.py dominium-registered-validation validate
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-RELABEL-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-RELABEL-01
strict old-label active-surface scan
strict local-absolute-path scan over active reports and task evidence
strict secret-like token scan over active reports and task evidence
py -3 .aide/scripts/aide_lite.py validate
git diff --check
git diff --cached --check
py -3 .aide/scripts/aide_lite.py commit check --latest
```
