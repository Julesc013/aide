# Next Batch

Selected next task:

```text
AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01
```

## Goal

Independently review install dry-run check reports, generated install plans, expected reports, path boundaries, managed-section expectations, hash references, no-apply proof, and capability labels.

## Why Selected

The install dry-run checks produced deterministic report-only evidence with warnings but no defects. Independent review is the next smallest safe step before any upgrade dry-run, fixture apply gate, or lifecycle harness widening.

## Allowed Paths

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01/**`
- install dry-run reports and evidence as read-only inputs
- deterministic validation/status report refreshes

## Review Gate

End at `needs_review`.

## Prompt Seed

Create `AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01` as an independent no-apply checkpoint for `AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-01`. Review the install dry-run reports, generated install plans, expected reports, path boundaries, managed-section expectations, hash references, no-apply proof, warnings, and capability labels. Do not execute install apply, lifecycle apply, scoped transaction apply against fixture targets, active repo apply, target repo mutation, branch/worktree mutation, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, or broad active-repo apply. Stop at `needs_review`.
