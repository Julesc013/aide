# Next Plan

Task: AIDE-CHECK-APPLY-00-transaction-model-review

## Next Queue Item

AIDE-APPLY-01-managed-section-patcher

## Required Boundary For AIDE-APPLY-01

- Start from reviewed AIDE-APPLY-00 transaction records.
- Preserve manual content through marker-aware managed-section logic.
- Keep real repository apply disabled unless a later reviewed queue item explicitly authorizes it.
- Keep rollback records as evidence unless a future rollback apply phase is reviewed.
- Do not mutate branches, worktrees, targets, GitHub, releases, providers, models, Gateway, or network state.

## Deferred

- Install/upgrade apply.
- Repair/rollback/uninstall apply.
- Branch/worktree orchestration.
- Gateway and live model routing.
- Release publication.
