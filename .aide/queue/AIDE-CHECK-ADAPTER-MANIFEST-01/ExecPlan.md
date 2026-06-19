# AIDE-CHECK-ADAPTER-MANIFEST-01 ExecPlan

## Objective

Create and process the AdapterManifest independent-check task only as far as
live queue authority permits.

## Scope

- Re-read live queue authority, PatchTransaction acceptance state, and
  AdapterManifest build state.
- Stop as `BLOCKED` if the AdapterManifest build is absent, incomplete,
  contradictory, failed, superseded, or not `PASS`/`PASS_WITH_WARNINGS`.
- Materialize task-local evidence and blocked check reports.
- Do not implement, repair, or independently validate AdapterManifest
  implementation artifacts because the build did not create them.

## Live Disposition

The check precondition is not met. `AIDE-BUILD-ADAPTER-MANIFEST-01` exists and
has complete evidence, but its result is `BLOCKED`, not `PASS` or
`PASS_WITH_WARNINGS`.

The immediate source chain records:

```text
AIDE-ACCEPT-PATCH-TRANSACTION-SCHEMA-01 BLOCKED
AIDE-BUILD-ADAPTER-MANIFEST-01         BLOCKED
```

The only serialized next task remains:

```text
AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01
```

## Milestones

- Live branch, HEAD, and worktree inspected.
- AdapterManifest build task and evidence inspected.
- PatchTransaction acceptance baseline inspected.
- Check blocked before AdapterManifest review.
- Blocked task packet and reports written.
- Task-local evidence written.
- Validation run for the blocked check packet.
- Task stopped at `needs_review`.

## Exit Criteria

The task exits with `BLOCKED`, no AdapterManifest check execution, no
implementation or repair, no forbidden operation, complete evidence, and exactly
one recommended next task:

```text
AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01
```
