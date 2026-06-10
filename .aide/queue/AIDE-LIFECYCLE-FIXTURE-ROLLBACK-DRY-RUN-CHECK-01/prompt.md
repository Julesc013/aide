# Prompt: AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-CHECK-01

Independently review `AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-01` and its report-only rollback dry-run evidence. Verify rollback dry-run reports, rollback record consumption, current-hash checks, inverse operation checks, rollback preconditions and stop conditions, manual preservation, protected path boundaries, no-rollback-execution proof, scoped executor interlock, capability labels, and validation evidence.

Do not implement or execute rollback apply, rollback execution, uninstall apply, uninstall execution, lifecycle apply, scoped transaction apply against fixture targets, fixture target mutation, active repo scoped apply mutation, target repo mutation, branch/worktree mutation, merge, push, promotion, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, or broad active-repo apply.

End at `needs_review` with checkpoint disposition `ACCEPTED_WITH_NOTES` and select exactly one next safe WorkUnit.
