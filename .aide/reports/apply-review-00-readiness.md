# AIDE-APPLY-01 Readiness

- classification: READY_FOR_AIDE_APPLY_01_WITH_WARNINGS
- next_task: AIDE-APPLY-01 - Managed Section Patcher
- allowed_posture: fixture-safe and review-gated
- real_repo_apply_allowed: false
- target_mutation_allowed: false
- branch_worktree_mutation_allowed: false
- provider_model_network_allowed: false

## Allowed Next Scope

- managed-section parser
- managed-section patcher
- marker detection
- manual-content preservation
- section hash capture
- conflict detection
- fixture-only patch apply in temp dirs
- transaction model integration
- tests, golden tasks, docs, and export-pack sync

## Forbidden Next Scope

- install/upgrade/repair/rollback/uninstall apply
- target repo mutation
- branch/worktree mutation
- merge/push/promotion
- release publication
- provider/model/network
- Gateway forwarding
- active repo transaction apply
