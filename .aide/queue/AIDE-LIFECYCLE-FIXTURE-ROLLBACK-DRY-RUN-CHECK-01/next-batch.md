# Next Batch

Selected next task: `AIDE-LIFECYCLE-FIXTURE-UNINSTALL-DRY-RUN-01`

Goal: Run report-only and dry-run uninstall planning checks against generated lifecycle fixture uninstall plans and expected reports, including delete/manual-content safety evidence, without implementing or executing uninstall apply.

Why selected:

- Rollback dry-run evidence has been independently checkpointed with `ACCEPTED_WITH_NOTES`.
- Uninstall dry-run remains the next missing lifecycle dry-run proof before proof-chain closure.
- The task can remain report-only and does not require lifecycle apply, rollback execution, scoped transaction fixture apply, active repo apply, target repo mutation, provider/model/Gateway/network calls, release work, or branch/worktree mutation.

Prerequisites:

- `AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-CHECK-01`
- `AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-01`
- `AIDE-LIFECYCLE-FIXTURE-ROLLBACK-RECORD-CHECK-01`
- `AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01`
- `AIDE-LIFECYCLE-SCHEMA-VALIDATOR-01`
- `AIDE-APPLY-02-scoped-transaction-executor-v0`

Forbidden operations remain install apply, upgrade apply, lifecycle repair apply, rollback apply, rollback execution, uninstall apply, uninstall execution, lifecycle apply, scoped transaction apply against fixture targets, fixture target mutation, active repo scoped apply mutation, target repo mutation, branch/worktree mutation, merge, push, promotion, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, broad active-repo apply, production-ready claims, and release-ready claims.
