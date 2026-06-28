# Finding Matrix

| Finding ID | Check Result | Evidence |
| --- | --- | --- |
| `distribution_apply_engine.update_plan_binding_not_enforced` | Closed | `missing-update-plan-binding` refuses with `distribution_apply_engine.update_plan_binding_missing` before temp workspace execution. |
| `distribution_apply_engine.rollback_bundle_binding_not_enforced` | Closed | `missing-rollback-bundle-binding` refuses with `distribution_apply_engine.rollback_bundle_binding_missing` before temp workspace execution. |
| `distribution_apply_engine.predecessor_mismatch_not_refused` | Closed | source distribution, project lock, ownership ledger, install record, and migration record mismatch scenarios refuse with `distribution_apply_engine.predecessor_mismatch`. |
| `distribution_apply_engine.run_without_accepted_context` | Closed | `run-without-accepted-context` refuses with `distribution_apply_engine.accepted_context_missing` before temp workspace execution. |

`material_finding_count`: `0`

`missing_evidence`: `0`
