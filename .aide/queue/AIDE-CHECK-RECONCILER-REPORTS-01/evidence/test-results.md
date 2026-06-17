# Test Results

Status: `PASS`

Focused tests:

- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_reconciler_reports.py`: PASS

Compile checks:

- `py -3 -m py_compile .aide/scripts/aide_lite.py`: PASS
- `py -3 -m py_compile core/reconciler/reconciler_reports.py`: PASS

JSON parsing:

- `py -3 -m json.tool .aide/reports/reconciler/reconciliation-report.json`: PASS
- `py -3 -m json.tool .aide/reports/reconciler/validation.json`: PASS
- `py -3 -m json.tool .aide/reports/reconciler/findings.json`: PASS
- `py -3 -m json.tool .aide/reports/reconciler/finding-taxonomy.json`: PASS
- `py -3 -m json.tool .aide/reports/reconciler-check/check-report.json`: PASS
