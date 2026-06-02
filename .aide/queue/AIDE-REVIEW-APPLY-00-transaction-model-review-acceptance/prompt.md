# Prompt: AIDE-REVIEW-APPLY-00

Review and accept the AIDE-APPLY-00 transaction model and AIDE-CHECK-APPLY-00 no-real-apply boundary checkpoint before AIDE-APPLY-01.

This is a review-gate WorkUnit only. It must decide whether AIDE may proceed to AIDE-APPLY-01 managed-section patcher work. It must not implement AIDE-APPLY-01 or introduce real apply behavior.

Required decisions:

- AIDE-APPLY-00 review decision.
- AIDE-CHECK-APPLY-00 review decision.
- AIDE-APPLY-01 readiness.
- No-real-apply boundary status.
- Warning disposition.
- Next task packet target.

Forbidden:

- target repo mutation
- active repo transaction apply
- install/repair/upgrade/rollback/uninstall apply
- branch/worktree mutation
- merge, push, promotion, tag, release, or publication
- GitHub API mutation
- provider/model/network calls
- Gateway forwarding
- AIDE-APPLY-01 implementation
