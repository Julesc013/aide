# Validation

Final validation status: `PASS_WITH_WARNINGS`

Primary Reconciler checks:

- `py -3 -m py_compile .aide/scripts/aide_lite.py`: PASS
- `py -3 -m py_compile core/reconciler/reconciler_reports.py`: PASS
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_reconciler_reports.py`: PASS
- `py -3 .aide/scripts/aide_lite.py reconciler status`: PASS_WITH_WARNINGS
- `py -3 .aide/scripts/aide_lite.py reconciler report`: PASS_WITH_WARNINGS
- `py -3 .aide/scripts/aide_lite.py reconciler validate`: PASS_WITH_WARNINGS

Generated report JSON parsing:

- `py -3 -m json.tool .aide/reports/reconciler/reconciliation-report.json`: PASS
- `py -3 -m json.tool .aide/reports/reconciler/validation.json`: PASS
- `py -3 -m json.tool .aide/reports/reconciler/findings.json`: PASS
- `py -3 -m json.tool .aide/reports/reconciler/finding-taxonomy.json`: PASS

Predecessor checks:

- `worker-run validate`: PASS
- `test-job validate`: PASS
- `reference-id validate`: PASS_WITH_WARNINGS
- `event-record validate`: PASS_WITH_WARNINGS
- `okf validate`: PASS_WITH_WARNINGS
- `okf lint`: PASS_WITH_WARNINGS
- broad `validate`: PASS

Task checks:

- `task inspect --task-id AIDE-BUILD-RECONCILER-REPORTS-01`: PASS
- `task evidence --task-id AIDE-BUILD-RECONCILER-REPORTS-01`: PASS

Git checks:

- `git diff --check`: PASS
- `git diff --cached --check`: PASS

Expected warnings are Reconciler findings, not blockers.
