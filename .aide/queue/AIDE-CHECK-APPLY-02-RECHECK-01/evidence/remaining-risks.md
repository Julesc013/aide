# Remaining Risks

Task: `AIDE-CHECK-APPLY-02-RECHECK-01`

## Executor Risks

- Multi-file atomic apply remains unimplemented; v0 blocks multi-mutating apply.
- Apply mode remains scoped and requires explicit plans, allowed paths, protected paths, operation allowlists, preimage hashes, postimage verification, staged-change records, and rollback-compatible records.
- Platform-specific reparse-point behavior should be revisited before any target-repo capability.

## Review Risks

- Historical `AIDE-CHECK-APPLY-02` still records `NEEDS_REPAIR`; this recheck records the accepted-with-notes superseding disposition for the repaired findings.
- AIDE filesystem status remains `needs_review` by convention; acceptance is recorded as a review disposition and queue evidence.

## Lifecycle Risks

- Install, upgrade, lifecycle repair, rollback/uninstall, target repo mutation, branch/worktree mutation, release, GitHub, provider/model, Gateway, network, and broad active-repo apply surfaces remain deferred and prohibited.

## Repo-Wide Validate Warning

- The prior repair warning is no longer reproduced. `py -3 .aide/scripts/aide_lite.py validate` now reports `status: PASS`.
- Classification: `FALSE_POSITIVE_OR_STALE_REPORT`.
- No separate generated-report self-reference repair is recommended from this recheck.

## Next Risk-Control Step

Run `AIDE-QUEUE-CLOSURE-02` to refresh the blocker graph and choose the next safe batch before lifecycle apply planning.
