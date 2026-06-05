# Next Batch

Selected next task:

```text
AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01
```

## Goal

Generate lifecycle fixture dry-run/report-only plans from the reviewed static fixture repository and lifecycle schemas without executing lifecycle apply.

## Why Selected

The fixture checkpoint accepted static fixture materialization with notes. The smallest safe next step is plan generation in report-only/dry-run mode so future tasks can compare generated plans against expected reports before any fixture apply authority is considered.

## Allowed Paths

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01/**`
- future plan-generator source files only if explicitly authorized by that task
- `.aide/examples/apply/lifecycle-fixtures/**` for read-only inputs unless that task explicitly authorizes generated plan artifacts under a fixture-report path
- `.aide/reports/lifecycle-fixtures/**`
- deterministic task/status report refreshes required by validation

## Protected Paths

`.git/**`, `.github/**`, `.aide.local/**`, secrets, credentials, target repositories, release roots, provider/model/Gateway files, branch/worktree automation files, active lifecycle apply implementation files, install/upgrade/repair/rollback/uninstall implementation files, scoped transaction executor implementation files, managed-section implementation files, and unrelated implementation roots.

## Forbidden Operations

No lifecycle apply implementation or execution, no scoped transaction apply against fixture targets, no install/upgrade/lifecycle repair/rollback/uninstall apply, no target repo mutation, no branch/worktree mutation, no merge, no push, no promotion, no release publication, no GitHub mutation, no provider/model calls, no Gateway calls, no network calls, no broad active-repo apply, no broad deletes, no broad moves, no production-ready claims, and no release-ready claims.

## Review Gate

End at `needs_review`.

## Prompt Seed

Create `AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01` as a no-apply WorkUnit that generates lifecycle fixture dry-run/report-only plans from the reviewed static lifecycle fixtures and lifecycle schemas. Do not execute lifecycle apply, scoped transaction apply against fixture targets, install/upgrade/lifecycle repair/rollback/uninstall apply, active repo apply, target repo mutation, branch/worktree mutation, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, or broad active-repo apply. End at `needs_review` with validation evidence and one next WorkUnit.
