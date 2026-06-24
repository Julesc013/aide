# Validation Commands

Commands run for this check:

```text
git status --short --branch
git log --oneline --decorate -8
git rev-parse 7f043d0
py -3 .aide\queue\AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01\evidence\independent-repair-check.py
py -3 -m py_compile core\execution\registered_process.py core\execution\provider.py core\protocol\process_invocation.py core\protocol\execution_receipt.py core\interop\dominium\registered_validation_backend.py .aide\scripts\tests\test_aide_registered_process_provider.py .aide\scripts\tests\test_aide_dominium_registered_validation_backend.py .aide\queue\AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01\evidence\independent-repair-check.py
py -3 .aide\scripts\tests\test_aide_registered_process_provider.py
py -3 .aide\scripts\tests\test_aide_dominium_registered_validation_backend.py
py -3 -m json.tool .aide\reports\registered-process-execution-provider-v0-repair-check\check-report.json
py -3 .aide\scripts\aide_lite.py validate
py -3 .aide\scripts\aide_lite.py task inspect --task-id AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01
py -3 .aide\scripts\aide_lite.py task evidence --task-id AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01
git diff --check
git diff --cached --check
```

Additional local-path and secret-like marker scans were run over this task and
report scope. They are summarized in `validation-results.md`.
