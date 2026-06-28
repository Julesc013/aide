# Build Summary

Result: `PASS_WITH_WARNINGS`

Proposed capability: `distribution_apply_engine_v0`

The build adds a fixture-only and temp-workspace-only distribution executor. It loads committed scenario fixtures, copies each target fixture into a temporary workspace, executes only planned and rollback-covered operations, preserves protected ownership classes, emits UpdateReceipt-shaped fixture output, verifies postimage digests, verifies rollback, and verifies canonical fixture files remain unchanged.

Warnings:

- DistributionApplyEngine v0 remains proposed until independent check and acceptance.
- Execution is limited to copied temporary fixture workspaces.
- The build is not real target apply, source repo self-update, release readiness, self-consumer fixture readiness, canary readiness, or provider/model/network authority.

Counters:

- material_finding_count: `0`
- missing_evidence: `0`
- scenario_count: `37`
- positive_scenario_count: `17`
- negative_scenario_count: `20`

Next task: `AIDE-CHECK-DISTRIBUTION-APPLY-ENGINE-V0-01`
