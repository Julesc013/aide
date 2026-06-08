# Expected Report Checks

Result: `PASS_WITH_WARNINGS`

Checked report evidence:

- 3 generated plan reports under `.aide/reports/lifecycle-fixture-plans/`.
- 2 static expected report examples under `.aide/examples/apply/lifecycle-fixtures/expected-reports/`.

Static expected report refs present:

- `upgrade-v2`
- `drift-detected`

Static expected report ref absent but non-blocking for this report-only check:

- `upgrade-manual-preserved`

Present static expected reports match generated plans for status, blocker labels, mutation state, `target_files_mutated=false`, empty `files_changed`, and `review_gate=needs_review`.

Detailed machine-readable evidence:

- `.aide/reports/lifecycle-fixture-upgrade-dry-run/upgrade-expected-report-checks.json`
