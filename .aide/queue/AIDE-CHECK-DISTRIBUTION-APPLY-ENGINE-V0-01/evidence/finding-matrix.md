# Finding Matrix

| Finding ID | Severity | Evidence | Required repair |
| --- | --- | --- | --- |
| `distribution_apply_engine.update_plan_binding_not_enforced` | material | Missing `update_plan_ref` still executes and emits receipt output. | Require an accepted UpdatePlan fixture ref before execution; fail closed if absent. |
| `distribution_apply_engine.rollback_bundle_binding_not_enforced` | material | Missing `rollback_bundle_ref` still executes and emits receipt output. | Require an accepted RollbackBundle fixture ref before execution; fail closed if absent. |
| `distribution_apply_engine.predecessor_mismatch_not_refused` | material | Mismatched source distribution, project lock, and ownership ledger refs still execute. | Validate predecessor refs against accepted fixture metadata and fail closed on mismatch. |
| `distribution_apply_engine.run_without_accepted_context` | material | A temp repo without UpdateReceipt acceptance evidence can run the scenario and emit receipt output. | Gate execution on accepted UpdateReceipt context, or prove equivalent accepted fixture context, before run. |

`missing_evidence` is `0`.
