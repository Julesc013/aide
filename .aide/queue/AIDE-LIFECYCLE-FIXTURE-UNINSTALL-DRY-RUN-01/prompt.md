# Prompt: AIDE-LIFECYCLE-FIXTURE-UNINSTALL-DRY-RUN-01

Run report-only and dry-run uninstall planning checks against generated lifecycle fixture uninstall plans and expected evidence. Verify uninstall scenario plans, generated plan reports, expected state, available expected reports, preimage/postimage hash references, manual preservation, broad-delete blocking, protected path boundaries, scoped executor interlock, and no-uninstall-execution proof.

Do not implement or execute install apply, upgrade apply, lifecycle repair apply, rollback apply, rollback execution, uninstall apply, uninstall execution, lifecycle apply, scoped transaction apply against fixture targets, fixture target mutation, active repo scoped apply mutation, target repo mutation, branch/worktree mutation, merge, push, promotion, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, or broad active-repo apply.

End at `needs_review` and select exactly one next WorkUnit.
