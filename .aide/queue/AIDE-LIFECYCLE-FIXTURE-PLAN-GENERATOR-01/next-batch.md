# Next Batch

Selected next task:

```text
AIDE-LIFECYCLE-FIXTURE-PLAN-CHECK-01
```

## Goal

Independently review generated lifecycle fixture plans, generated plan reports, no-apply proof, scoped executor interlock, capability labels, and validation evidence.

## Why Selected

The generated plan artifacts are substantial enough to require independent review before any future dry-run execution or planner widening. This keeps the next step report-only and does not widen authority.

## Allowed Paths

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-PLAN-CHECK-01/**`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- `.aide/examples/apply/lifecycle-fixtures/generated-plans/**` read-only
- `.aide/reports/lifecycle-fixture-plans/**` read-only
- deterministic validation/status report refreshes

## Protected Paths

`.git/**`, `.github/**`, `.aide.local/**`, secrets, credentials, target repositories, release roots, provider/model/Gateway files, branch/worktree automation files, active lifecycle apply implementation files, install/upgrade/repair/rollback/uninstall implementation files, scoped transaction executor implementation files, managed-section implementation files, and unrelated implementation roots.

## Forbidden Operations

No lifecycle apply implementation or execution, no scoped transaction apply against fixture targets, no install/upgrade/lifecycle repair/rollback/uninstall apply, no target repo mutation, no branch/worktree mutation, no merge, no push, no promotion, no release publication, no GitHub mutation, no provider/model calls, no Gateway calls, no network calls, no broad active-repo apply, no broad deletes, no broad moves, no production-ready claims, and no release-ready claims.

## Review Gate

End at `needs_review`.

## Prompt Seed

Create `AIDE-LIFECYCLE-FIXTURE-PLAN-CHECK-01` as an independent no-apply checkpoint for generated lifecycle fixture plans. Review `.aide/examples/apply/lifecycle-fixtures/generated-plans/**`, `.aide/reports/lifecycle-fixture-plans/**`, `AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01` evidence, no-apply proof, scoped executor interlock, and capability labels. Do not execute lifecycle apply, scoped transaction apply against fixture targets, install/upgrade/lifecycle repair/rollback/uninstall apply, active repo apply, target repo mutation, branch/worktree mutation, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, or broad active-repo apply. End at `needs_review` with disposition and one next WorkUnit.
