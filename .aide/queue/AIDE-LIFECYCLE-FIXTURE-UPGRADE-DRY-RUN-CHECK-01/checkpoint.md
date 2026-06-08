# Checkpoint

Disposition: `ACCEPTED_WITH_NOTES`

`AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-01` is accepted with notes as a report-only upgrade dry-run checkpoint. The review verified:

- All three upgrade scenarios are covered: `upgrade-v2`, `upgrade-manual-preserved`, and `drift-detected`.
- Generated upgrade plans and generated plan reports parse and align with scenario IDs, expected statuses, and expected blocker labels.
- Static expected reports are present and coherent for `upgrade-v2` and `drift-detected`.
- The static expected report ref is absent for `upgrade-manual-preserved`; this is non-blocking for checkpoint acceptance because generated plan report evidence, static hashes, managed-section preservation checks, path checks, and no-apply proof exist, but it remains a repair-worthy evidence gap.
- Drift detection preserves `BLOCKED_DRIFT_DETECTED` before mutation.
- Managed-section evidence preserves manual content outside generated markers.
- Hash references match expected preimage and postimage SHA-256 values.
- No-apply proof preserves `target_files_mutated=false`, `upgrade_apply_executed=false`, `lifecycle_apply_executed=false`, `scoped_transaction_apply_executed=false`, and `rollback_execution_implemented=false`.
- Capability labels remain review-gated and planned-only for upgrade apply and lifecycle apply.

This checkpoint does not authorize install apply, upgrade apply, lifecycle repair apply, fixture apply, lifecycle apply, active repo apply, target repo apply, rollback execution, uninstall/delete execution, release work, provider/model/Gateway/network calls, GitHub mutation, branch/worktree mutation, or broad active-repo apply.
