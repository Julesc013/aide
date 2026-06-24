# Validation Evidence

Result: `PASS_WITH_WARNINGS`

Commands run:

- `py -3 .aide/queue/AIDE-CHECK-AIDE-SELF-VALIDATION-PROCESS-ADAPTER-01/evidence/independent_self_validation_check.py` - passed, generated `check-report.json` with `material_finding_count: 0`.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-AIDE-SELF-VALIDATION-PROCESS-ADAPTER-01` - passed, `classification: complete`, `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-AIDE-SELF-VALIDATION-PROCESS-ADAPTER-01` - passed, six evidence files available, none missing.
- `py -3 .aide/scripts/aide_lite.py aide-self-validation-process-adapter validate` - passed, `PASS_WITH_WARNINGS`, `error_count: 0`.
- `py -3 -m compileall core/interop/aide core/execution core/protocol .aide/scripts/tests` - passed.
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_self_validation_process_adapter.py` - passed, 5 tests.
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_registered_process_provider.py` - passed, 8 tests.
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_dominium_registered_validation_backend.py` - passed, 7 tests.
- `py -3 .aide/scripts/aide_lite.py validate` - passed.
- `rg -n -P "(?<![A-Za-z0-9])[A-Za-z]:[\\/]" .aide/reports/aide-self-validation-process-adapter-check .aide/queue/AIDE-CHECK-AIDE-SELF-VALIDATION-PROCESS-ADAPTER-01` - no matches.
- `rg -n -P "(?i)\b(sk|ghp|github_pat|xox[baprs]?)-[A-Za-z0-9_\-]{8,}" .aide/reports/aide-self-validation-process-adapter-check .aide/queue/AIDE-CHECK-AIDE-SELF-VALIDATION-PROCESS-ADAPTER-01` - no matches.
- `git diff --name-only -- .aide/reports/aide-self-validation-process-adapter` - no source build report churn.
- `git diff --check` - passed.
- `git diff --cached --check` - passed after staging the check-owned files.
- `py -3 .aide/scripts/aide_lite.py commit check --latest` - passed after commit message amendment.
