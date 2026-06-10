# Expected Report Coverage

The selected scenario has static expected report coverage:

- `.aide/examples/apply/lifecycle-fixtures/expected-reports/install-managed-section.report.json`

Known warning:

- Six previously missing expected report files were added by `AIDE-LIFECYCLE-EXPECTED-REPORT-GAP-REPAIR-01`.
- Generated plan embedded `expected_report_ref` fields remain deferred for those repaired scenarios, but this does not affect the selected `install-managed-section` scenario because its generated plan already has a static expected report ref.
