# Adversarial Probes

The check reran isolated probes against the apply engine without writing implementation or fixture files. The probes mutated scenario data in memory or used a temporary repo root.

All six probes should have failed closed. All six instead returned `PASS_WITH_WARNINGS`, generated UpdateReceipt-shaped output, and verified rollback:

| Probe | Expected refusal | Observed |
| --- | --- | --- |
| missing `update_plan_ref` | `distribution_apply_engine.missing_update_plan_ref_refused` | `PASS_WITH_WARNINGS` |
| missing `rollback_bundle_ref` | `distribution_apply_engine.missing_rollback_bundle_ref_refused` | `PASS_WITH_WARNINGS` |
| mismatched `source_distribution_ref` | `distribution_apply_engine.source_distribution_mismatch_refused` | `PASS_WITH_WARNINGS` |
| mismatched `project_lock_ref` | `distribution_apply_engine.project_lock_mismatch_refused` | `PASS_WITH_WARNINGS` |
| mismatched `ownership_ledger_ref` | `distribution_apply_engine.ownership_ledger_mismatch_refused` | `PASS_WITH_WARNINGS` |
| missing accepted UpdateReceipt context | `distribution_apply_engine.update_receipt_acceptance_missing` | `PASS_WITH_WARNINGS` |

These probes support four material findings because they show the executor is not yet strongly bound to accepted predecessor context.
