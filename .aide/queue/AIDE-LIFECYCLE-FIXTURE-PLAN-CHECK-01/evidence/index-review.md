# Index Review

Index path: `.aide/examples/apply/lifecycle-fixtures/generated-plans/plan-index.json`

Result: `PASS_WITH_NOTES`

- Parse result: PASS.
- Scenario count: 13.
- Plans generated: 13.
- Duplicate/missing scenario result: PASS.
- Plan paths: PASS.
- Report paths: PASS.
- Top-level no-apply fields: `target_files_mutated=false`, `lifecycle_apply_implemented=false`, `lifecycle_apply_executed=false`, `scoped_transaction_apply_executed=false`, `rollback_execution_implemented=false`.
- Capability labels: plan-generated, dry-run-planned, fixture-plan-generated, schema-validated, locally-validated, report-backed, review-gated, planned-only for lifecycle apply.
- Authority/overclaim result: PASS.

Note: the index does not duplicate `target_files_mutated_expected=false`; all 13 generated plans carry that field explicitly and false.
