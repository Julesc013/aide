# Validation

## Result

`PASS_WITH_WARNINGS`

## Commands

- `py -3 -m core.reconciler.report_index`
- `py -3 -m unittest core.reconciler.tests.test_report_index`
- `py -3 -m py_compile core/reconciler/report_index.py core/reconciler/tests/test_report_index.py`
- `validate_report_index_reports('.')`
- deterministic rerun hash comparison for index and report outputs
- JSON parse for `.aide/reports/index.yaml` and report JSON files
- Markdown/JSON finding agreement
- `git diff --check`
- `git diff --cached --check`
- `py -3 .aide/scripts/aide_lite.py doctor`
- `py -3 .aide/scripts/aide_lite.py validate`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-REPORT-INDEX-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-REPORT-INDEX-01`

## Observed Results

- Focused tests passed: 3 tests.
- Python compile passed.
- Report-index validator returned `validated: true`.
- Deterministic rerun comparison passed.
- Self-output paths are explicitly excluded.
- GeneratedOutputLedger input is recorded as provisional and unaccepted.
- No indexed report was moved, renamed, rewritten, repaired, normalized, or
  deleted.
