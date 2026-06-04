# Next Batch

Selected next task:

```text
AIDE-LIFECYCLE-SCHEMA-VALIDATOR-01
```

## Goal

Implement or wire local validation for the lifecycle manifest, lifecycle plan, lifecycle report, rollback-compatible record schemas, and non-mutating lifecycle examples.

## Why Selected

This task created schema and example files, but it did not implement a lifecycle schema validator. The smallest safe next step is to validate those contracts locally before fixture materialization or fixture lifecycle dry-run planning.

## Allowed Paths

- `.aide/queue/AIDE-LIFECYCLE-SCHEMA-VALIDATOR-01/**`
- `.aide/apply/lifecycle-*.schema.json`
- `.aide/examples/apply/lifecycle/**`
- `.aide/scripts/aide_lite.py` only if the validator is explicitly authorized by that future task
- `.aide/scripts/tests/test_aide_lifecycle_schema_validator.py` only if explicitly authorized
- `.aide/reports/lifecycle-schema-*.md`
- `.aide/reports/lifecycle-schema-*.json`
- `.aide/queue/index.yaml` if live queue policy requires it

## Protected Paths

`.git/**`, `.github/**`, `.aide.local/**`, secrets, credentials, target repositories, release roots, provider/model/Gateway files, branch/worktree automation files, active lifecycle apply implementation files, install/upgrade/repair/rollback/uninstall implementation files, and unrelated implementation roots.

## Forbidden Operations

No lifecycle apply implementation or execution, install apply, upgrade apply, lifecycle repair apply, rollback/uninstall apply, target repo mutation, branch/worktree mutation, merge, push, promotion, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, broad active-repo apply, broad deletes, broad moves, production-ready claims, or release-ready claims.

## Review Gate

End at `needs_review` with validation evidence.

## Prompt Seed

Create `AIDE-LIFECYCLE-SCHEMA-VALIDATOR-01` as a narrow queue WorkUnit that validates the lifecycle manifest, lifecycle plan, lifecycle report, rollback-compatible lifecycle record schemas, and `.aide/examples/apply/lifecycle/**` examples. Use local tooling only. Do not implement or execute lifecycle apply, do not materialize fixture targets, do not mutate target repositories or branches/worktrees, do not call GitHub, providers/models, Gateway, or network services, and do not mark lifecycle capability production-ready or release-ready. End at `needs_review` with evidence and one next WorkUnit.
