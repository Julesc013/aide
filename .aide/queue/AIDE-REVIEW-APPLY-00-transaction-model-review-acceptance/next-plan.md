# Next Plan

## Selected Next Task

AIDE-APPLY-01 - Managed Section Patcher

## Entry Conditions

- Human review accepts this AIDE-REVIEW-APPLY-00 packet or accepts it with notes.
- AIDE-APPLY-01 gets its own bounded queue packet and ExecPlan.
- The no-real-apply boundary remains explicit.

## Required Boundary

AIDE-APPLY-01 may implement fixture-safe managed-section parsing and patching behavior for tests and temp-dir fixtures. It must not mutate target repositories, branches, worktrees, releases, providers, models, network, Gateway, or install/repair/upgrade/rollback/uninstall state.
