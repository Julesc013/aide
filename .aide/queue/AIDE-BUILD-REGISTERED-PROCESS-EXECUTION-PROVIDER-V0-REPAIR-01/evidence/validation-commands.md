# Validation Commands

```text
git status --short --branch
py -3 -m py_compile core\execution\registered_process.py .aide\scripts\tests\test_aide_registered_process_provider.py .aide\scripts\tests\test_aide_dominium_registered_validation_backend.py
py -3 .aide\scripts\tests\test_aide_registered_process_provider.py
py -3 .aide\scripts\tests\test_aide_dominium_registered_validation_backend.py
rg -n -i "dominium|validation\.run|AIDE-BUILD|AIDE-CHECK|registered-validation|\.aide|queue|report|write_text|write_json" core\execution\registered_process.py core\execution\provider.py
py -3 .aide\scripts\aide_lite.py validate
py -3 -m json.tool .aide\reports\registered-process-execution-provider-v0-repair\repair-report.json
py -3 .aide\scripts\aide_lite.py task inspect --task-id AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01
py -3 .aide\scripts\aide_lite.py task evidence --task-id AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01
rg -n "[A-Z]:[\\/]" core\execution\registered_process.py .aide\scripts\tests\test_aide_registered_process_provider.py .aide\queue\AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01 .aide\reports\registered-process-execution-provider-v0-repair
rg -n --pcre2 "(?i)(github_pat|ghp_[A-Za-z0-9_]{8,}|sk-[A-Za-z0-9_-]{20,}|api[_-]?key\s*[:=]|password\s*[:=]|token\s*[:=])" core\execution\registered_process.py .aide\scripts\tests\test_aide_registered_process_provider.py .aide\queue\AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01 .aide\reports\registered-process-execution-provider-v0-repair
git diff -U0 -- PLANS.md IMPLEMENT.md | rg -n "[A-Z]:[\\/]"
git diff --check
git diff --cached --check
```
