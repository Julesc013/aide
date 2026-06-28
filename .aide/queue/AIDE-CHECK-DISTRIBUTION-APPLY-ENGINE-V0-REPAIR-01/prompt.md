# Prompt: AIDE-CHECK-DISTRIBUTION-APPLY-ENGINE-V0-REPAIR-01

Independently check the DistributionApplyEngine v0 repair.

Verify closure of:

- `distribution_apply_engine.update_plan_binding_not_enforced`
- `distribution_apply_engine.rollback_bundle_binding_not_enforced`
- `distribution_apply_engine.predecessor_mismatch_not_refused`
- `distribution_apply_engine.run_without_accepted_context`

Authority:

- Check only.
- Do not repair implementation.
- Do not accept DistributionApplyEngine v0.
- Do not start self-consumer fixture or canaries.
- Do not perform real target apply, source repo apply, release publication, provider/model/network calls, or external repo mutation.

Expected next task if this check passes:

`AIDE-ACCEPT-DISTRIBUTION-APPLY-ENGINE-V0-01`
