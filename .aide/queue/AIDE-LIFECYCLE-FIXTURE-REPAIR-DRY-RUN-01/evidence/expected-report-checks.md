# Expected Report Checks

Report: `.aide/reports/lifecycle-fixture-repair-dry-run/repair-expected-report-checks.json`

Result: `PASS_WITH_WARNINGS`

Reports and expected evidence checked:

- `.aide/reports/lifecycle-fixture-plans/repair-plan-missing-marker.plan-report.json`
- `.aide/reports/lifecycle-fixture-plans/repair-plan-malformed-marker.plan-report.json`
- `.aide/examples/apply/lifecycle-fixtures/expected/repair-plan-missing-marker/README.md`
- `.aide/examples/apply/lifecycle-fixtures/expected/repair-plan-malformed-marker/README.md`

Findings:

- Generated plan reports parse as JSON.
- Generated plan reports match fixture metadata for expected status and expected blocker.
- Expected-state README files state the same blocked status and blocker labels.
- No repair report claims `target_files_mutated=true`.
- No repair report claims lifecycle repair apply, lifecycle apply, scoped transaction apply, or rollback execution occurred.

Warning:

- Static `expected_report_ref` values are absent for both repair scenarios. This is non-blocking for this report-only dry-run check, but should be reviewed in `AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01`.
