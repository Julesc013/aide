# AIDE-BUILD-CONTEXTPACK-V2-01 ExecPlan

## Objective

Create and process the ContextPack v2 build task only as far as live queue
authority permits.

## Scope

- Re-read live queue authority, PatchTransaction acceptance state, and
  AdapterManifest build/check/acceptance state.
- Stop as `BLOCKED` if AdapterManifest acceptance is not `ACCEPTED` or
  `ACCEPTED_WITH_WARNINGS`, or if PatchTransaction acceptance is not accepted.
- Materialize task-local evidence and blocked build reports.
- Do not create ContextPack v2 schema, helper, CLI dispatch, focused tests, or
  projections because the prerequisite chain is blocked.

## Live Disposition

The build precondition is not met. The immediate source chain records:

```text
AIDE-ACCEPT-PATCH-TRANSACTION-SCHEMA-01 BLOCKED
AIDE-BUILD-ADAPTER-MANIFEST-01         BLOCKED
AIDE-CHECK-ADAPTER-MANIFEST-01         BLOCKED
AIDE-ACCEPT-ADAPTER-MANIFEST-01        BLOCKED
```

The only serialized next task remains:

```text
AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01
```

## Milestones

- Live branch, HEAD, and worktree inspected.
- AdapterManifest build/check/acceptance chain inspected.
- PatchTransaction acceptance baseline inspected.
- ContextPack v2 build blocked before implementation.
- Blocked task packet and reports written.
- Task-local evidence written.
- Validation run for the blocked build packet.
- Task stopped at `needs_review`.

## Exit Criteria

The task exits with `BLOCKED`, no ContextPack v2 implementation, no forbidden
operation, complete evidence, and exactly one recommended next task:

```text
AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01
```
