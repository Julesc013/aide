# AIDE-QUEUE-CLOSURE-01 Next Batch

## Selected Batch

Exactly one task:

```text
AIDE-APPLY-02-IMPLEMENT
```

## Why This Is Safe Now

- AIDE-APPLY-02 has a live queue item.
- AIDE-APPLY-02 has an ExecPlan.
- AIDE-APPLY-02 has explicit allowed paths.
- AIDE-APPLY-02 has protected paths and forbidden operations.
- AIDE-APPLY-02 has validation and evidence requirements.
- AIDE-APPLY-02 requires dry-run/report mode, preimage hash checks, postimage verification, and rollback-compatible records before any scoped mutation can be accepted.
- The work is local and queue-scoped.
- The work does not require target mutation, branch/worktree mutation, network/provider/Gateway/GitHub calls, release publication, or install/upgrade/repair/rollback/uninstall apply.

## Why Not Batch More

- AIDE-CHECK-APPLY-02 depends on AIDE-APPLY-02 implementation evidence.
- Queue-closure implementation depends on a reviewed decision after the scoped executor checkpoint.
- Task OS stale report repair is lower priority than implementing the already authorized apply substrate task.
- Target/release/provider/Gateway work remains prohibited or deferred.

## Prompt Seed

Task ID: `AIDE-APPLY-02-IMPLEMENT`

Implement `AIDE-APPLY-02 - Scoped Transaction Executor v0` using only `.aide/queue/AIDE-APPLY-02-scoped-transaction-executor-v0/task.yaml`, `ExecPlan.md`, `allowed-paths.md`, `protected-paths.md`, `forbidden-operations.md`, `validation-checklist.md`, and `review-gate.md` as authority. Include dry-run/report mode, preimage hash checks, postimage verification, rollback-compatible records, targeted validation, and evidence. Do not widen scope. End at `needs_review` and preserve all forbidden operations.
