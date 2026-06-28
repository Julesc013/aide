# Finding Closure

| Finding ID | Repair |
| --- | --- |
| `distribution_apply_engine.update_plan_binding_not_enforced` | `apply_context.validate_accepted_context` now refuses missing scenario or context `update_plan_ref` before execution with `distribution_apply_engine.update_plan_binding_missing`. |
| `distribution_apply_engine.rollback_bundle_binding_not_enforced` | The accepted context gate now refuses missing scenario or context `rollback_bundle_ref` before execution with `distribution_apply_engine.rollback_bundle_binding_missing`. |
| `distribution_apply_engine.predecessor_mismatch_not_refused` | The accepted context gate now checks distribution, project lock, ownership ledger, install record, migration record, target project, UpdatePlan, and RollbackBundle refs against accepted context constants and refuses mismatches with `distribution_apply_engine.predecessor_mismatch`. |
| `distribution_apply_engine.run_without_accepted_context` | Every executable scenario now requires `accepted_context.required: true`, accepted status, and valid predecessor acceptance reports before any temp workspace execution. Missing context refuses with `distribution_apply_engine.accepted_context_missing`. |

Refused context-binding scenarios suppress successful UpdateReceipt fixture output, leave `operation_results` empty, and do not enter temp workspace execution.
