# Expected Report Review

Result: `PASS_WITH_WARNINGS`

Generated reports checked for expected upgrade report alignment:

- 3 generated plan reports under `.aide/reports/lifecycle-fixture-plans/`.
- 10 upgrade dry-run reports under `.aide/reports/lifecycle-fixture-upgrade-dry-run/`.

Static expected reports checked:

- `.aide/examples/apply/lifecycle-fixtures/expected-reports/upgrade-v2.report.json`
- `.aide/examples/apply/lifecycle-fixtures/expected-reports/drift-detected.report.json`

Missing expected report refs:

- `upgrade-manual-preserved`

Classification:

- non-blocking for this checkpoint
- repair-worthy evidence gap

Status/blocker match: PASS.

Mutation-state result: PASS.

Overclaim result: PASS.

Defects: none.
