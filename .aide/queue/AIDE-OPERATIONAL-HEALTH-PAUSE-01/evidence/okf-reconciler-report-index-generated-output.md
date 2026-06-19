# OKF, Reconciler, ReportIndex, And GeneratedOutputLedger

Commands and sources:

- `py -3 .aide/scripts/aide_lite.py okf validate`: `PASS_WITH_WARNINGS`
- `py -3 .aide/scripts/aide_lite.py okf lint`: `PASS_WITH_WARNINGS`
- `py -3 .aide/scripts/aide_lite.py reconciler status`: `PASS_WITH_WARNINGS`
- `py -3 .aide/scripts/aide_lite.py reconciler validate`: `PASS_WITH_WARNINGS`
- `.aide/reports/self-management/report-index.json`: parseable
- `.aide/reports/self-management/generated-output-ledger.json`: parseable
- `.aide/reports/self-management/track-b-b1-barrier.json`: parseable

Findings:

- OKF lint reports `stale_context_findings_count: 1`.
- Reconciler reports `findings_count: 4`, `report_only: true`, and
  `repair_implemented: false`.
- ReportIndex result is `PASS_WITH_WARNINGS`, with 479 indexed reports and 70
  ambiguous records.
- GeneratedOutputLedger result is `PASS_WITH_WARNINGS`, with 1381 classified
  candidates and 67 unknown-generator records.
- Track B B1 barrier result is `PASS_WITH_WARNINGS`, `b1_complete: true`, and
  `blocking_findings: 0`.
- No `report-index` or `generated-output` AIDE Lite command group exists in
  the current command surface; status is report-backed.
