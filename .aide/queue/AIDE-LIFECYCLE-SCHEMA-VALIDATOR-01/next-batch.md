# Next Batch

Selected next task:

```text
AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01
```

## Goal

Materialize the lifecycle fixture directory tree and static fixture inputs expected by the lifecycle schema layer, without executing lifecycle apply.

## Why Selected

The lifecycle schema validator now validates schemas and non-mutating examples locally. The smallest next blocker is missing physical fixture content for future lifecycle dry-run proof work.

## Allowed Paths

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01/**`
- `.aide/examples/apply/lifecycle-fixtures/**`
- `.aide/reports/lifecycle-fixtures/**`
- `.aide/examples/apply/lifecycle/**` only for fixture spec reference repair if explicitly authorized
- `.aide/reports/lifecycle-schema-*.md`
- `.aide/reports/lifecycle-schema-*.json`
- `.aide/queue/index.yaml` if live queue policy requires it

## Protected Paths

`.git/**`, `.github/**`, `.aide.local/**`, secrets, credentials, target repositories, release roots, provider/model/Gateway files, branch/worktree automation files, active lifecycle apply implementation files, install/upgrade/repair/rollback/uninstall implementation files, and unrelated implementation roots.

## Forbidden Operations

No lifecycle apply implementation or execution, install apply, upgrade apply, lifecycle repair apply, rollback/uninstall apply, target repo mutation, branch/worktree mutation, merge, push, promotion, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, broad active-repo apply, broad deletes, broad moves, production-ready claims, or release-ready claims.

## Review Gate

End at `needs_review` with fixture materialization evidence.

## Prompt Seed

Create `AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01` as a narrow queue WorkUnit that materializes static lifecycle fixture inputs under `.aide/examples/apply/lifecycle-fixtures/**` and report/evidence directories under authorized lifecycle fixture paths. Do not implement or execute lifecycle apply, install apply, upgrade apply, lifecycle repair apply, rollback/uninstall apply, active repo apply, target repo mutation, branch/worktree mutation, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, or broad active-repo apply. End at `needs_review` with evidence and one next WorkUnit.
