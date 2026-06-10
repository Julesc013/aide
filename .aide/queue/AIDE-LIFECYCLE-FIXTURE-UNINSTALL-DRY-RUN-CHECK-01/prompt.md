# Prompt: AIDE-LIFECYCLE-FIXTURE-UNINSTALL-DRY-RUN-CHECK-01

Independently review `AIDE-LIFECYCLE-FIXTURE-UNINSTALL-DRY-RUN-01` and its report-only uninstall dry-run evidence. Verify generated uninstall plans, plan reports, expected state, expected report coverage, manual preservation, broad-delete blocking, protected path handling, no-uninstall-execution proof, scoped executor interlock, capability labels, and validation evidence.

Do not implement or execute install apply, upgrade apply, lifecycle repair apply, rollback apply, rollback execution, uninstall apply, uninstall execution, lifecycle apply, scoped transaction apply against fixture targets, fixture target mutation, active repo scoped apply mutation, target repo mutation, branch/worktree mutation, merge, push, promotion, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, or broad active-repo apply.

End at `needs_review` with an explicit checkpoint disposition and the next single safe WorkUnit.
