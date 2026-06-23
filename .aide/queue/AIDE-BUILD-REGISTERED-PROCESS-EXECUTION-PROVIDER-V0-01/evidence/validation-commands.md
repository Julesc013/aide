# Validation Commands

Planned and executed validation commands:

```text
py -3 -m py_compile core\protocol\process_invocation.py core\protocol\execution_receipt.py core\execution\__init__.py core\execution\provider.py core\execution\registered_process.py core\interop\dominium\registered_validation_backend.py .aide\scripts\tests\test_aide_registered_process_provider.py .aide\scripts\tests\test_aide_dominium_registered_validation_backend.py
py -3 .aide\scripts\tests\test_aide_registered_process_provider.py
py -3 .aide\scripts\tests\test_aide_dominium_registered_validation_backend.py
py -3 .aide\scripts\aide_lite.py dominium-registered-validation validate
$json_files = Get-ChildItem -Recurse -File .aide\reports\registered-process-execution-provider-v0, .aide\queue\AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01 -Filter *.json; foreach ($file in $json_files) { Get-Content -Raw -LiteralPath $file.FullName | ConvertFrom-Json > $null }
rg -n "dominium|Dominium|AIDE-BUILD|AIDE-CHECK|registered-validation|validation.run" core\execution core\protocol\process_invocation.py core\protocol\execution_receipt.py
rg -n "[A-Z]:[\\/]" .aide\queue\AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01 .aide\reports\registered-process-execution-provider-v0
rg -n --pcre2 <secret-like-value-pattern> .aide\queue\AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01 .aide\reports\registered-process-execution-provider-v0
py -3 .aide\scripts\aide_lite.py task inspect --task-id AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01
py -3 .aide\scripts\aide_lite.py task evidence --task-id AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01
py -3 .aide\scripts\aide_lite.py validate
git -C <dominium-root> status --short --branch
git diff --check
git diff --cached --check
py -3 .aide\scripts\aide_lite.py commit check --message <structured Phase 4 commit message>
py -3 .aide\scripts\aide_lite.py commit check --latest
```
