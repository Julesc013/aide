# Validation Commands

Planned and executed validation commands:

```text
py -3 .aide\queue\AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01\evidence\independent-provider-check.py
py -3 -m py_compile .aide\queue\AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01\evidence\independent-provider-check.py
py -3 .aide\scripts\tests\test_aide_registered_process_provider.py
py -3 .aide\scripts\tests\test_aide_dominium_registered_validation_backend.py
py -3 .aide\scripts\aide_lite.py dominium-registered-validation validate
py -3 .aide\scripts\aide_lite.py task inspect --task-id AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01
py -3 .aide\scripts\aide_lite.py task evidence --task-id AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01
py -3 .aide\scripts\aide_lite.py validate
git -C <dominium-root> status --short --branch
rg -n "[A-Z]:[\\/]" .aide\queue\AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01 .aide\reports\registered-process-execution-provider-v0-check
rg -n --pcre2 <secret-like-value-pattern> .aide\queue\AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01 .aide\reports\registered-process-execution-provider-v0-check
git diff --check
git diff --cached --check
py -3 .aide\scripts\aide_lite.py commit check --message <structured check commit message>
py -3 .aide\scripts\aide_lite.py commit check --latest
```
