# AIDE-CHECK-APPLY-01 Prompt

Perform one bounded AIDE repository checkpoint audit for `AIDE-APPLY-01 - Managed Section Patcher`.

This is review, audit, verification, warning disposition, and next-plan work only. It must not implement AIDE-APPLY-02, patch active repository files as product behavior, mutate target repositories, mutate branches or worktrees, publish releases, call GitHub APIs, call providers/models/network, or enable install/repair/upgrade/rollback/uninstall apply behavior.

Required decision points:

- AIDE-APPLY-01 decision.
- Managed-section patcher readiness.
- AIDE-APPLY-02 readiness.
- Warning classification.
- Exact next task.

Expected passing decision:

- `AIDE-APPLY-01`: `ACCEPTED_WITH_NOTES`
- Managed-section readiness: `READY_FOR_SCOPED_TRANSACTION_EXECUTOR_WITH_WARNINGS`
- AIDE-APPLY-02 readiness: `READY_FOR_AIDE_APPLY_02_WITH_WARNINGS`
- Next task: `AIDE-APPLY-02 - Scoped Transaction Executor v0`

Required outputs are the queue packet, review reports, validation evidence, warning disposition, and latest task packet.
