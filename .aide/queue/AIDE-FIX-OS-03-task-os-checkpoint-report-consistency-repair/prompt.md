# Prompt

Repair the report-only Task OS checkpoint and readiness report consistency blocker found by AIDE-CHECK-OS-01.

Fix exactly these issues:

- `task status` and related latest-task parsing must preserve `AIDE-FIX-OS-03` and resolve it to the canonical queue item rather than reducing it to `X-OS-03`.
- `checkpoint status` must inspect X-OS-02 queue truth and stop hardcoding `missing_or_not_done`.
- `task-os-next-plan` and command status must stop selecting or recommending X-OS-02 after X-OS-02 is complete.
- AIDE-CHECK-OS-01 readiness logic must be rerunnable and coherent.
- The latest task packet may point to AIDE-APPLY-00 only after this repair validates.

Forbidden: no AIDE-APPLY-00 implementation, no apply behavior, no task/repair execution, no target mutation, no branch/worktree mutation, no merge/push/promotion, no release publication, no GitHub API mutation, no provider/model/network calls, and no Gateway forwarding.
