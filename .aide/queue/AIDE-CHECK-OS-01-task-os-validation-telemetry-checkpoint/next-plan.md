# Next Plan

## Selected Next Task

`AIDE-FIX-OS-03 - Task OS checkpoint report consistency repair`

## Objective

Repair report-only Task OS generated report logic so checkpoint and next-plan outputs reflect current queue truth after X-OS-02 and AIDE-CHECK-OS-01.

## Required Scope

- Update latest-task parsing to prefer current/goal task identity instead of the first historical X-OS reference in packet text.
- Update `checkpoint status` to inspect X-OS-02 status instead of hardcoding `missing_or_not_done`.
- Update `task-os-next-plan` and command status recommendation after X-OS-02 is complete.
- Add tests and golden coverage for AIDE-CHECK-OS-01 to repair-task transition and later AIDE-APPLY-00 readiness.

## Forbidden Scope

No apply behavior, branch/worktree mutation, merge, push, promotion, target mutation, release publication, provider/model/network calls, Gateway forwarding, or AIDE-APPLY-00 implementation.

## After Repair

Rerun this checkpoint or a compact checkpoint verification. If the repaired reports match repo truth, generate the next packet for `AIDE-APPLY-00 - Transaction Model`.
