# Next Batch

Selected next task:

`AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-01`

Goal:

Run report-only/dry-run upgrade planning checks against generated upgrade fixture plans and expected reports, with no lifecycle apply execution, no scoped transaction fixture apply, no fixture target mutation, no active repo apply, and no target repo mutation.

Why selected:

The install dry-run checkpoint is accepted with notes. The two missing static expected report refs are non-blocking for the install checkpoint, and upgrade dry-run is the next smallest lifecycle planning surface before any fixture apply gate.

Allowed paths:

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-01/**`
- upgrade dry-run report output path to be defined by that task
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- deterministic status/validation report refreshes

Forbidden operations:

- no install apply, upgrade apply, lifecycle repair apply, rollback apply, uninstall apply, lifecycle apply, scoped transaction apply against fixture targets, fixture target mutation, active repo scoped apply mutation, target repo mutation, branch/worktree mutation, merge, push, promotion, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, or broad active-repo apply.

Review gate: `needs_review`

Prompt seed:

Create `AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-01` as a report-only/dry-run WorkUnit for generated upgrade fixture plans and expected reports. Review upgrade scenarios, expected reports, path boundaries, managed-section preservation, hash references, no-apply proof, capability labels, and scoped executor interlock. Do not execute lifecycle apply, upgrade apply, scoped transaction apply against fixture targets, fixture target mutation, active repo apply, target repo mutation, branch/worktree mutation, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, or broad active-repo apply. Stop at `needs_review`.
