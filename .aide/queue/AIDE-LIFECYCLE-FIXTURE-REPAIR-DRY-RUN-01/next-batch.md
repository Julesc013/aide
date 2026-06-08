# Next Batch

Selected next task:

`AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01`

Goal:

Independently review lifecycle repair dry-run check reports, generated repair plans, missing marker and malformed marker evidence, expected repair report evidence, drift evidence, path boundaries, hash references, no-apply proof, scoped executor interlock, and capability labels.

Why selected:

The repair dry-run check passed with warnings and stopped at `needs_review`. An independent checkpoint is the smallest safe next task before rollback/uninstall dry-run or any fixture apply gate.

Allowed paths:

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01/**`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- deterministic status/validation report refreshes

Forbidden operations:

- no install apply, upgrade apply, lifecycle repair apply execution, rollback apply, uninstall apply, lifecycle apply, scoped transaction apply against fixture targets, fixture target mutation, active repo scoped apply mutation, target repo mutation, branch/worktree mutation, merge, push, promotion, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, or broad active-repo apply.

Review gate: `needs_review`

Prompt seed:

Create `AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01` as an independent checkpoint for `AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-01`. Review repair dry-run reports, generated repair plans, missing marker and malformed marker evidence, expected report evidence, drift context, path boundaries, managed-section marker behavior, hash references, no-apply proof, scoped executor interlock, capability labels, validation, and evidence. Do not implement or execute lifecycle repair apply, lifecycle apply, install apply, upgrade apply, rollback apply, uninstall apply, scoped transaction apply against fixture targets, fixture target mutation, active repo apply, target repo mutation, branch/worktree mutation, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, or broad active-repo apply. Stop at `needs_review`.
