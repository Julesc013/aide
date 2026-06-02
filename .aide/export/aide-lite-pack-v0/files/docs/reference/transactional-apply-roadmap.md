# Transactional Apply Roadmap

AIDE-APPLY-00 defines transaction contracts only. It intentionally stops before real apply behavior.

## Phase Order

1. AIDE-APPLY-00 defines schemas, policies, examples, fixture planning, fixture verification, and evidence records.
2. AIDE-APPLY-01 may define a managed-section patcher if it remains fixture-safe and review-gated.
3. Later phases may consider staged file operations only after ownership, preimage, postimage, rollback, conflict, and safety gates are reviewed.
4. Real repository apply, target repository apply, destructive operations, branch/worktree automation, and install/repair/upgrade/rollback/uninstall apply remain separate future review items.

No roadmap entry here authorizes apply behavior.
