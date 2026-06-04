# Next Batch

Selected next task:

```text
AIDE-LIFECYCLE-FIXTURE-CHECK-01
```

## Goal

Independently review the materialized static lifecycle fixtures, fixture metadata, expected reports, rollback-compatible records, hash evidence, validator interlock, and no-apply boundaries before lifecycle fixture plan generation.

## Why Selected

Fixture materialization is substantial and creates many static inputs for later dry-run proof tasks. A review/check WorkUnit is the smallest safe next batch because it does not widen authority, does not execute lifecycle apply, and can validate that fixture coverage and capability labels are honest before generating plans.

## Allowed Paths

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-CHECK-01/**`
- `.aide/examples/apply/lifecycle-fixtures/**` for read/review evidence only unless repair is explicitly authorized
- `.aide/reports/lifecycle-fixtures/**`
- `.aide/reports/lifecycle-schema-*.md`
- `.aide/reports/lifecycle-schema-*.json`
- deterministic task/status report refreshes required by validation

## Protected Paths

`.git/**`, `.github/**`, `.aide.local/**`, secrets, credentials, target repositories, release roots, provider/model/Gateway files, branch/worktree automation files, active lifecycle apply implementation files, install/upgrade/repair/rollback/uninstall implementation files, and unrelated implementation roots.

## Forbidden Operations

No lifecycle apply implementation or execution, no scoped transaction apply against fixture targets, no install/upgrade/lifecycle repair/rollback/uninstall apply, no target repo mutation, no branch/worktree mutation, no merge, no push, no promotion, no release publication, no GitHub mutation, no provider/model calls, no Gateway calls, no network calls, no broad active-repo apply, no broad deletes, no broad moves, no production-ready claims, and no release-ready claims.

## Review Gate

End at `needs_review`.

## Prompt Seed

Review `AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01` as an independent no-apply checkpoint. Verify the static lifecycle fixture tree, scenario metadata, expected reports, rollback-compatible records, hash evidence, lifecycle-schema validation results, no-apply proof, capability labels, and forbidden-operation boundaries. Do not implement or execute lifecycle apply, scoped transaction apply against fixture targets, install/upgrade/lifecycle repair/rollback/uninstall apply, target repo mutation, branch/worktree mutation, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, or broad active-repo apply. End at `needs_review` with one next WorkUnit.
