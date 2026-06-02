# AIDE-APPLY-01 Readiness

## Classification

READY_FOR_AIDE_APPLY_01_WITH_WARNINGS

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

- install apply
- upgrade apply
- repair apply
- rollback/uninstall apply
- target repo mutation
- branch/worktree mutation
- merge/push/promotion
- release publication
- provider/model/network
- Gateway forwarding
- active repo transaction apply

## Conclusion

AIDE-APPLY-01 is the correct next implementation step after this review gate is accepted. It must remain fixture-safe and review-gated unless a future queue item explicitly authorizes real apply.
