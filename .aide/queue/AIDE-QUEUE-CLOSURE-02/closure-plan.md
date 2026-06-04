# AIDE-QUEUE-CLOSURE-02 Closure Plan

## A. Resolvable Now

### AIDE-TASK-OS-STATUS-REPAIR-01

- goal: Repair stale Task OS current/latest-task reporting and related current-task guidance after AIDE-APPLY-02 accepted-with-notes.
- reason: `task status` reports `latest_task_id: AIDE-APPLY-02` as missing even though the indexed live task is `AIDE-APPLY-02-scoped-transaction-executor-v0` and is accepted with notes.
- blockers resolved: Task OS latest-task selector drift, stale latest-task packet, stale generated next-action guidance, and possibly stale README next-work guidance if included in the allowlist.
- prerequisites: AIDE-APPLY-02 accepted-with-notes evidence, AIDE-CHECK-APPLY-02-RECHECK-01 review, queue policy, and a narrow task-local ExecPlan.
- allowed paths: proposed `.aide/queue/AIDE-TASK-OS-STATUS-REPAIR-01/**`, `.aide/context/latest-task-packet.md`, `.aide/reports/task-os-*.md`, `.aide/reports/task-os-*.json`, `.aide/queue/index.yaml`, and only additional docs/report paths explicitly justified by that task.
- protected paths: `.git/**`, `.github/**`, `.aide.local/**`, secrets and credential files, target repositories, release publication files, provider/model/Gateway integration files, branch/worktree automation files, and implementation files outside the repair task.
- forbidden operations: install apply, upgrade apply, lifecycle repair apply, rollback/uninstall apply, target repo mutation, branch/worktree mutation, merge, push, promotion, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, broad active-repo apply, broad deletes, broad moves, and self-promotion from review-gated to accepted/production-ready.
- validation commands: `git status --short --branch`, `git diff --check`, `py -3 .aide/scripts/aide_lite.py task status`, `py -3 .aide/scripts/aide_lite.py validate`, targeted Task OS command/status checks, boundary searches, parse checks for changed machine-readable files, and changed-file secret scan.
- expected evidence: changed files, before/after Task OS status, latest-task packet disposition, generated report churn disposition, validation log, boundary confirmation, remaining risks, and review gate.
- review gate: `needs_review`.
- status after completion: `needs_review`.
- batching: do not batch; current-task truth repair should be isolated.

## B. Requires Queue Authorization

### AIDE-APPLY-LIFECYCLE-PLAN-01

- reason: AIDE-APPLY-02 is accepted with notes, so lifecycle planning may be proposed, but stale Task OS current truth should be repaired first.
- unblock: complete `AIDE-TASK-OS-STATUS-REPAIR-01`, then create a planning-only lifecycle task.

### AIDE-QUEUE-CLOSURE-AUTOMATION-PLAN-01

- reason: Queue closure as reusable automation is not authorized by this report-only task.
- unblock: create a planning/authorization WorkUnit after current queue truth and apply lifecycle planning are stable.

## C. Requires Human Decision

No branch-ahead decision is required by live evidence in this pass because `git rev-list --left-right --count origin/main...HEAD` returned `0 0`. Push, merge, promotion, release publication, and branch/worktree mutation remain prohibited without explicit authority.

Human review may still be needed for review-gated backlog disposition and any product sequencing choice that would move target, release, provider/model, Gateway, or network work forward.

## D. Prohibited Until Policy Changes

- install apply
- upgrade apply
- lifecycle repair apply
- rollback/uninstall apply
- target repo mutation
- branch/worktree mutation
- merge
- push
- promotion
- release publication
- GitHub mutation
- provider/model calls
- Gateway calls
- network calls
- broad active-repo apply

These are graph prohibition nodes. They are not closure tasks.

## E. Deferred By Design

- target repo adoption and target mutation;
- XCHECK, Dominium, and Eureka reconciliation;
- Gateway/provider live calls;
- release publication;
- install/upgrade/lifecycle repair/rollback/uninstall apply execution;
- broad active-repo apply;
- queue-closure automation implementation.

These remain behind current-task truth repair, review gates, explicit queue authorization, and capability reality updates.
