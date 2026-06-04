# Changed Files

Task: `AIDE-CHECK-APPLY-02-RECHECK-01`

## Recheck Artifacts

- `.aide/queue/AIDE-CHECK-APPLY-02-RECHECK-01/task.yaml`: review-only queue task metadata and allowed boundaries.
- `.aide/queue/AIDE-CHECK-APPLY-02-RECHECK-01/ExecPlan.md`: durable recheck plan and progress.
- `.aide/queue/AIDE-CHECK-APPLY-02-RECHECK-01/prompt.md`: task prompt seed.
- `.aide/queue/AIDE-CHECK-APPLY-02-RECHECK-01/status.yaml`: recheck result and disposition.
- `.aide/queue/AIDE-CHECK-APPLY-02-RECHECK-01/review.md`: accepted-with-notes review.
- `.aide/queue/AIDE-CHECK-APPLY-02-RECHECK-01/checkpoint.md`: checkpoint decision.
- `.aide/queue/AIDE-CHECK-APPLY-02-RECHECK-01/evidence/*.md`: validation, repair recheck, static review, boundary review, capability reality, and remaining risk evidence.

## Queue Status References

- `.aide/queue/AIDE-APPLY-02-scoped-transaction-executor-v0/task.yaml`: records `accepted_with_notes` planning state and next action.
- `.aide/queue/AIDE-APPLY-02-scoped-transaction-executor-v0/status.yaml`: records the recheck disposition while preserving `status: needs_review`.
- `.aide/queue/AIDE-APPLY-02-REPAIR-01/status.yaml`: records the recheck disposition against the repair.
- `.aide/queue/index.yaml`: registers this recheck task and updates AIDE-APPLY-02/AIDE-APPLY-02-REPAIR-01 summaries.

## Generated Reports

The following report families were refreshed by validation/status commands and are within the recheck allowlist:

- `.aide/reports/scoped-transaction-executor-*`
- `.aide/reports/managed-section-*`
- `.aide/reports/transaction-*`
- `.aide/reports/task-os-*`
- `.aide/reports/current-aide-roadmap.md`

## Implementation Files

No implementation files were changed by this recheck.
