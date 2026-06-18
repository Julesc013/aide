# Validation Results

## Result

`PASS_WITH_WARNINGS`

## Observed Results

- `py -3 -m unittest core.reconciler.tests.test_generated_output_ledger`: PASS, 4 tests.
- `py -3 -m py_compile core/reconciler/generated_output_ledger.py core/reconciler/tests/test_generated_output_ledger.py`: PASS.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-GENERATED-OUTPUT-LEDGER-01`: PASS, `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-GENERATED-OUTPUT-LEDGER-01`: PASS, no missing evidence.
- JSON/YAML parse for `.aide/ledgers/generated-output.yaml`, `generated-output-ledger.json`, and `generated-output-ledger.findings.json`: PASS.
- Detached temp-clone baseline replay at `af3156a`: PASS, 1,381 candidates.
- In-memory current HEAD observation: PASS_WITH_WARNINGS, 1,385 candidates explained by later ReportIndex outputs.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-GENERATED-OUTPUT-LEDGER-01`: PASS, `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-GENERATED-OUTPUT-LEDGER-01`: PASS, no missing evidence.
- `git diff --check`: PASS_WITH_WARNING, known `.aide/queue/index.yaml` CRLF warning only.
