# Next Batch

Selected next task:

`AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-01`

Goal:

Run report-only/dry-run lifecycle repair planning checks against repair fixture scenarios, including missing marker and malformed marker cases, with no lifecycle repair apply execution or scoped transaction fixture apply.

Why selected:

The upgrade dry-run checkpoint is accepted with notes and the missing `upgrade-manual-preserved` static expected report ref is non-blocking for this checkpoint. The smallest safe next lifecycle surface is repair dry-run planning, not fixture apply or active repo apply.

Allowed paths:

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-01/**`
- repair dry-run report output path to be defined by that task
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- deterministic status/validation report refreshes

Forbidden operations:

- no install apply, upgrade apply, lifecycle repair apply execution, rollback apply, uninstall apply, lifecycle apply, scoped transaction apply against fixture targets, fixture target mutation, active repo scoped apply mutation, target repo mutation, branch/worktree mutation, merge, push, promotion, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, or broad active-repo apply.

Review gate: `needs_review`

Prompt seed:

Create `AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-01` as a report-only/dry-run WorkUnit for lifecycle repair fixture planning checks. Review repair fixture scenarios such as missing marker and malformed marker cases, expected blockers, generated plans, path boundaries, managed-section safety, hash references, no-apply proof, scoped executor interlock, capability labels, validation, and evidence. Do not implement or execute lifecycle repair apply, upgrade apply, install apply, rollback apply, uninstall apply, lifecycle apply, scoped transaction apply against fixture targets, fixture target mutation, active repo apply, target repo mutation, branch/worktree mutation, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, or broad active-repo apply. Stop at `needs_review`.
