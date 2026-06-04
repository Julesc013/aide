# Next Batch

Selected next task:

```text
AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01
```

## Goal

Define lifecycle manifest, lifecycle transaction plan, lifecycle report, rollback-record, and fixture repository shape for future install, upgrade, repair, rollback, and uninstall proof.

## Why This Is Safe Now

- It is schema, fixture-shape, and planning work only.
- It does not execute lifecycle apply.
- It does not mutate active AIDE repo files through the scoped executor.
- It does not mutate target repositories.
- It does not require branch/worktree mutation, release publication, GitHub mutation, provider/model calls, Gateway calls, or network calls.
- It creates the missing contract layer before fixture install or rollback proof.

## Prerequisites

- `AIDE-APPLY-LIFECYCLE-PLAN-01` reviewed or accepted with notes.
- Current scoped executor status remains review-gated and not production-ready.
- Q43-Q46 no-apply lifecycle models remain the source planning surfaces.

## Allowed Paths

- `.aide/queue/AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01/**`
- narrow lifecycle schema/fixture paths explicitly authorized by that future task
- generated reports explicitly produced by validation commands
- `.aide/queue/index.yaml` if live queue policy requires it

## Protected Paths

- `.git/**`
- `.github/**`
- `.aide.local/**`
- secrets and credential files
- target repositories
- release publication files
- provider/model/Gateway files
- branch/worktree automation files
- active lifecycle apply implementation files unless separately authorized

## Forbidden Operations

No lifecycle apply execution, install apply, upgrade apply, lifecycle repair apply, rollback/uninstall apply, target repo mutation, branch/worktree mutation, merge, push, promotion, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, broad active-repo apply, broad deletes, or broad moves.

## Review Gate

End at `needs_review`.
