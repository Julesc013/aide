# Generated Output And Report Health

## ReportIndex

- source report: `.aide/reports/self-management/report-index.json`
- result: `PASS_WITH_WARNINGS`
- indexed_report_count: 479
- ambiguous_count: 70
- canonical: false for all indexed records
- command group: no `report-index` command group exists in current AIDE Lite

## GeneratedOutputLedger

- source report: `.aide/reports/self-management/generated-output-ledger.json`
- result: `PASS_WITH_WARNINGS`
- classified_count: 1381
- unknown_count: 67
- command group: no `generated-output` command group exists in current AIDE Lite

## Disposition

Report and generated-output volume creates navigation and freshness debt. The
current records are parseable and warning-class. This is not a blocker for
PatchTransaction if the next task does not reorganize reports, promote
generated output to canonical truth, or apply changes.
