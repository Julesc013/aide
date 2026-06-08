# Next Batch

Selected next task:

`AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-CHECK-01`

Goal:

Independently review upgrade dry-run check reports, generated upgrade plans, expected reports, path boundaries, managed-section expectations, drift detection, hash references, no-apply proof, scoped executor interlock, and capability labels.

Why selected:

The upgrade dry-run WorkUnit is report-backed and complete with one non-blocking evidence warning. A checkpoint review is the smallest safe next batch before lifecycle repair dry-run planning or any future fixture apply gate.

Allowed paths:

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-CHECK-01/**`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- deterministic status/validation report refreshes

Protected paths:

- `.git/**`, `.github/**`, `.aide.local/**`, secret and credential paths
- target repositories
- release roots
- provider/model/Gateway files
- branch/worktree automation files
- active lifecycle apply implementation files
- scoped transaction executor and managed-section implementation files
- fixture target files and generated upgrade plans unless a future repair task explicitly authorizes them

Forbidden operations:

- no install apply, upgrade apply, lifecycle repair apply, rollback apply, uninstall apply, lifecycle apply, scoped transaction apply against fixture targets, fixture target mutation, active repo scoped apply mutation, target repo mutation, branch/worktree mutation, merge, push, promotion, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, or broad active-repo apply.

Review gate: `needs_review`

Prompt seed:

Create `AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-CHECK-01` as an independent checkpoint review of `AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-01`. Review the upgrade dry-run reports, generated upgrade plans, expected reports where present, the missing `upgrade-manual-preserved` static expected report warning, path boundaries, managed-section preservation, drift detection, preimage and postimage hash references, no-apply proof, scoped executor interlock, capability labels, validation, and evidence. Do not implement or execute upgrade apply, lifecycle apply, scoped transaction apply against fixture targets, fixture target mutation, active repo apply, target repo mutation, branch/worktree mutation, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, or broad active-repo apply. Stop at `needs_review`.
