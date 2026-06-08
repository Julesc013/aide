# Next Batch

Selected next task:

```text
AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-01
```

## Goal

Run report-only/dry-run install planning checks against generated install fixture plans and expected reports without lifecycle apply execution or scoped transaction fixture apply.

## Why Selected

The generated fixture plan set is accepted with notes, and the next smallest safety-preserving step is to check install-phase dry-run/report behavior against the generated plan artifacts. This stays within no-apply lifecycle evidence and does not widen authority to fixture apply, active repo apply, target repo apply, rollback execution, uninstall/delete execution, release work, provider/model/Gateway/network calls, or branch/worktree mutation.

## Allowed Paths

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-01/**`
- future task-local evidence and reports explicitly authorized by that WorkUnit
- generated install fixture plans and expected reports as read-only inputs
- deterministic validation/status report refreshes

## Review Gate

End at `needs_review`.

## Prompt Seed

Create `AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-01` as a no-apply WorkUnit that runs report-only/dry-run install planning checks against the accepted generated lifecycle fixture plans and expected reports. Use generated install scenarios as read-only inputs, confirm path boundaries, managed-section expectations, preimage/postimage references, no-mutation flags, capability labels, and evidence output, and do not execute lifecycle apply, scoped transaction apply against fixture targets, active repo apply, target repo mutation, branch/worktree mutation, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, or broad active-repo apply. Stop at `needs_review`.
