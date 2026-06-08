# Expected Report Checks

Result: `PASS_WITH_WARNINGS`

Checked report evidence:

- 5 generated plan reports under `.aide/reports/lifecycle-fixture-plans/`.
- 3 static expected report examples under `.aide/examples/apply/lifecycle-fixtures/expected-reports/`.

Static expected report refs present:

- `install-managed-section`
- `protected-path-blocked`
- `traversal-blocked`

Static expected report refs absent but non-blocking for this report-only check:

- `install-clean`
- `install-existing-manual-preserved`

All generated plan reports preserve `target_files_mutated=false`, `lifecycle_apply_executed=false`, `scoped_transaction_apply_executed=false`, `rollback_execution_implemented=false`, and `review_gate=needs_review`.

Detailed machine-readable evidence:

- `.aide/reports/lifecycle-fixture-install-dry-run/install-expected-report-checks.json`
