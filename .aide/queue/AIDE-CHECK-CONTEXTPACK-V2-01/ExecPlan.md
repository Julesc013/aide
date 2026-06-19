# AIDE-CHECK-CONTEXTPACK-V2-01 ExecPlan

## Objective

Create and process the ContextPack v2 independent-check task only as far as
live queue authority permits.

## Scope

- Re-read live queue authority, ContextPack v2 build state, AdapterManifest
  acceptance state, and PatchTransaction acceptance state.
- Stop as `BLOCKED` if the ContextPack v2 build is absent, incomplete,
  contradictory, failed, superseded, or not `PASS`/`PASS_WITH_WARNINGS`.
- Materialize task-local evidence and blocked check reports.
- Do not implement, repair, or independently validate ContextPack v2
  implementation artifacts because the build did not create them.

## Live Disposition

The check precondition is not met. `AIDE-BUILD-CONTEXTPACK-V2-01` exists and
has complete evidence, but its result is `BLOCKED`, not `PASS` or
`PASS_WITH_WARNINGS`.

The immediate source chain records:

```text
AIDE-ACCEPT-PATCH-TRANSACTION-SCHEMA-01 BLOCKED
AIDE-ACCEPT-ADAPTER-MANIFEST-01          BLOCKED
AIDE-BUILD-CONTEXTPACK-V2-01             BLOCKED
```

The only serialized next task remains:

```text
AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01
```

## Milestones

- Live branch, HEAD, and worktree inspected.
- ContextPack v2 build task and evidence inspected.
- AdapterManifest and PatchTransaction acceptance baselines inspected.
- Check blocked before ContextPack v2 review.
- Blocked task packet and reports written.
- Task-local evidence written.
- Validation run for the blocked check packet.
- Task stopped at `needs_review`.

## Exit Criteria

The task exits with `BLOCKED`, no ContextPack v2 check execution, no
implementation or repair, no forbidden operation, complete evidence, and exactly
one recommended next task:

```text
AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01
```
