# Validation Results

## Result

`PASS_WITH_WARNINGS`

## Observed Results

- `py -3 -m unittest core.reconciler.tests.test_report_index`: PASS, 3 tests.
- `py -3 -m py_compile core/reconciler/report_index.py core/reconciler/tests/test_report_index.py`: PASS.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-REPORT-INDEX-01`: PASS, `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-REPORT-INDEX-01`: PASS, no missing evidence.
- JSON/YAML parse for `.aide/reports/index.yaml`, `report-index.json`, and `report-index.findings.json`: PASS.
- Detached temp-clone baseline replay at `bdfa1b7`: PASS, 479 reports and 70 ambiguity records.
- In-memory current HEAD observation: PASS_WITH_WARNINGS, 484 reports explained by later wave-2 outputs.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-REPORT-INDEX-01`: PASS, `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-REPORT-INDEX-01`: PASS, no missing evidence.
- `git diff --check`: PASS_WITH_WARNING, known `.aide/queue/index.yaml` CRLF warning only.
