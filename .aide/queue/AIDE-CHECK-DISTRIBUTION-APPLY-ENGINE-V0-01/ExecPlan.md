# AIDE-CHECK-DISTRIBUTION-APPLY-ENGINE-V0-01 ExecPlan

## Objective

Independently check `AIDE-BUILD-DISTRIBUTION-APPLY-ENGINE-V0-01` as a fixture-only, temp-workspace-only execution capability before acceptance.

## Scope

Allowed writes are limited to this check task packet, check reports, `.aide/queue/index.yaml`, `PLANS.md`, and `IMPLEMENT.md`.

Implementation repair, acceptance, self-consumer fixture work, canaries, releases, target mutation, source repo apply, provider/model/network calls, and branch/worktree automation are out of scope.

## Plan

1. Confirm live git and queue truth.
2. Inspect the build task, build evidence, reports, implementation, fixtures, focused tests, and predecessor acceptance chain.
3. Run normal validation for syntax, focused tests, CLI commands, predecessor regressions, Q43-Q48 no-apply/no-publish validators, and broad validation.
4. Run adversarial probes for missing binding, mismatched predecessor refs, and accepted-context gaps.
5. Record material findings and recommend a bounded repair task if any fail-closed behavior is missing.
6. Stop at `needs_review`.

## Result

`REQUEST_CHANGES`.

The build is structurally complete and its standard validations pass, but the independent check found four material semantic findings:

- `distribution_apply_engine.update_plan_binding_not_enforced`
- `distribution_apply_engine.rollback_bundle_binding_not_enforced`
- `distribution_apply_engine.predecessor_mismatch_not_refused`
- `distribution_apply_engine.run_without_accepted_context`

## Next

`AIDE-BUILD-DISTRIBUTION-APPLY-ENGINE-V0-REPAIR-01`
