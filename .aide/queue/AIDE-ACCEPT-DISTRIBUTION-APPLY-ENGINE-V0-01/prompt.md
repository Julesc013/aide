# Prompt

Create and process `AIDE-ACCEPT-DISTRIBUTION-APPLY-ENGINE-V0-01`.

Repo truth outranks this prompt. Inspect the live checkout before acting.

## Mission

Accept DistributionApplyEngine v0 as a fixture-only, temp-workspace-only distribution execution capability if and only if the build/check/repair/repair-check chain remains complete and evidence remains intact.

## Authority

Acceptance only.

Do not modify DistributionApplyEngine implementation. Do not repair implementation defects. Do not start the AIDE self-consumer fixture. Do not start project canaries. Do not perform real target apply, source repo apply, install/update/migration/rollback/repair/uninstall apply against a real target, release generation, tags, uploads, GitHub Releases, provider/model/network calls, branch/worktree automation, ScreenSave/Eureka/Dominium mutation, or external repository mutation.

## Acceptance Objectives

Confirm the predecessor chain is complete, the latest independent repair-check is `PASS` or `PASS_WITH_WARNINGS`, `material_finding_count` is `0`, `missing_evidence` is `0`, and the original four material findings are closed:

- `distribution_apply_engine.update_plan_binding_not_enforced`
- `distribution_apply_engine.rollback_bundle_binding_not_enforced`
- `distribution_apply_engine.predecessor_mismatch_not_refused`
- `distribution_apply_engine.run_without_accepted_context`

Accept only fixture-only, temp-workspace-only DistributionApplyEngine v0 and record accepted context-binding enforcement, UpdatePlan binding, RollbackBundle binding, predecessor-match enforcement, refusal reason codes, operation classes, fixture scenarios, canonical-fixture preservation, temp-workspace isolation, rollback verification, UpdateReceipt generation, explicit non-capabilities, and exactly one next task: `AIDE-BUILD-AIDE-SELF-CONSUMER-FIXTURE-V0-01`.
