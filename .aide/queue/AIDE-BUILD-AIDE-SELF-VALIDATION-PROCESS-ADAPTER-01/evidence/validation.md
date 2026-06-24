# Validation Evidence

Result: `PASS_WITH_WARNINGS`

The final committed adapter reports record:

- `process_call_count: 1`
- `result_origin: aide_lite_validate_stdout`
- `workspace_state_unchanged: true`
- `mutation_observation: none_detected_within_probe_coverage`
- `missing_evidence: 0`
- `recommended_next_task: AIDE-CHECK-AIDE-SELF-VALIDATION-PROCESS-ADAPTER-01`

Commands run:

```text
py -3 .aide/scripts/aide_lite.py aide-self-validation-process-adapter run
py -3 .aide/scripts/aide_lite.py aide-self-validation-process-adapter validate
py -3 -m compileall core/interop/aide core/execution core/protocol .aide/scripts/tests
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_self_validation_process_adapter.py
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_registered_process_provider.py
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_dominium_registered_validation_backend.py
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-AIDE-SELF-VALIDATION-PROCESS-ADAPTER-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-AIDE-SELF-VALIDATION-PROCESS-ADAPTER-01
py -3 .aide/scripts/aide_lite.py validate
rg -n -P "(?<![A-Za-z0-9])[A-Za-z]:[\\/]" .aide/reports/aide-self-validation-process-adapter .aide/queue/AIDE-BUILD-AIDE-SELF-VALIDATION-PROCESS-ADAPTER-01 core/interop/aide .aide/scripts/tests/test_aide_self_validation_process_adapter.py
rg -n -P "(?i)\b(sk|ghp|github_pat|xox[baprs]?)-[A-Za-z0-9_\-]{8,}" .aide/reports/aide-self-validation-process-adapter .aide/queue/AIDE-BUILD-AIDE-SELF-VALIDATION-PROCESS-ADAPTER-01 core/interop/aide .aide/scripts/tests/test_aide_self_validation_process_adapter.py
git diff --check
git diff --cached --check
```

Observed outcomes:

- adapter run: `PASS_WITH_WARNINGS`
- adapter report validation: `PASS_WITH_WARNINGS`
- compileall: passed
- focused self-adapter tests: passed, 5 tests
- focused registered-process provider tests: passed, 8 tests
- focused Dominium registered-validation parity tests: passed, 7 tests
- task inspect: `classification: complete`, `missing_evidence: 0`
- task evidence: three files available, no missing files
- broad AIDE Lite validate: `PASS`
- absolute local path scan: no matches
- secret-like scan: no matches
- `git diff --check`: passed
- `git diff --cached --check`: passed
