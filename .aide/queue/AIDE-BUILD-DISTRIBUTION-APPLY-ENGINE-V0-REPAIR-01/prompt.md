# Prompt: AIDE-BUILD-DISTRIBUTION-APPLY-ENGINE-V0-REPAIR-01

Repair DistributionApplyEngine v0 so fixture execution is impossible unless the selected scenario has a complete accepted context binding to an accepted UpdatePlan, accepted RollbackBundle, and matching accepted predecessor records.

Material findings repaired:

- `distribution_apply_engine.update_plan_binding_not_enforced`
- `distribution_apply_engine.rollback_bundle_binding_not_enforced`
- `distribution_apply_engine.predecessor_mismatch_not_refused`
- `distribution_apply_engine.run_without_accepted_context`

Authority:

- Repair only DistributionApplyEngine v0 boundary enforcement.
- Stop at `needs_review`.
- Do not accept DistributionApplyEngine.
- Do not start repair-check.
- Do not start self-consumer fixture.
- Do not mutate real target repositories or apply to the source repo.
- Do not create release archives, tags, uploads, or GitHub Releases.
- Do not call provider/model/network services.

Expected next task after a passing repair:

`AIDE-CHECK-DISTRIBUTION-APPLY-ENGINE-V0-REPAIR-01`
