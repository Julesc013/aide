# AIDE-QUEUE-CLOSURE-01 Closure Plan

## A. Resolvable Now

### AIDE-APPLY-02-IMPLEMENT

- goal: Implement scoped transaction executor v0 only.
- reason: `AIDE-APPLY-02-scoped-transaction-executor-v0` is pending and authorized for implementation.
- blockers resolved: READY node for AIDE-APPLY-02; enables later `AIDE-CHECK-APPLY-02`.
- prerequisites: AIDE-APPLY-00, AIDE-CHECK-APPLY-00, AIDE-REVIEW-APPLY-00, AIDE-APPLY-01, AIDE-CHECK-APPLY-01, and AIDE-APPLY-02 authorization packet.
- allowed paths: exactly those in `.aide/queue/AIDE-APPLY-02-scoped-transaction-executor-v0/allowed-paths.md`.
- protected paths: exactly those in `.aide/queue/AIDE-APPLY-02-scoped-transaction-executor-v0/protected-paths.md`.
- forbidden operations: exactly those in `.aide/queue/AIDE-APPLY-02-scoped-transaction-executor-v0/forbidden-operations.md`.
- validation commands: AIDE-APPLY-02 validation checklist, targeted tests, managed-section status/validate/fixture-verify, transaction status/validate/fixture-verify, `git diff --check`, boundary search, secret scan.
- expected evidence: changed files, validation, remaining risks, command surface, no-real-apply boundary, rollback/staged-change proof, fixture proof, capability reality, next checkpoint handoff.
- review gate: `queue_review_required`.
- status after completion: `needs_review`.
- batching: do not batch; implementation has its own review gate.

## B. Requires Queue Authorization

### AIDE-CHECK-APPLY-02

- reason: Required after AIDE-APPLY-02 implementation, but no queue item exists yet.
- unblock: create after AIDE-APPLY-02 reaches `needs_review`.

### AIDE-QUEUE-CLOSURE-02

- reason: Implementing queue-closure as a reusable core capability requires schemas/commands/tests and is not authorized by this report-only task.
- unblock: create after AIDE-CHECK-APPLY-02 decides the executor is safe enough for closure-command implementation.

### Task OS Current/Wave Repair

- reason: generated `task current`, `wave plan`, and checkpoint status surfaces lag behind live apply queue state.
- unblock: create a narrow repair task if stale surfaces remain after AIDE-APPLY-02 implementation/checkpoint.

## C. Requires Human Decision

### Local Branch Ahead Of Origin

- reason: branch is `main...origin/main [ahead 1]` after the AIDE-APPLY-02 authorization commit.
- decision needed: whether and when to push or integrate remains outside this task; push is prohibited without explicit authority.

### Promote Closure To Core Capability

- reason: the user requested queue closure as a core capability, but live repo authority only supports this report/planning task now.
- decision needed: approve a future implementation queue item after apply safety is checkpointed.

## D. Prohibited Until Policy Changes

- install apply
- upgrade apply
- repair apply
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
- Gateway/provider live calls;
- release publication;
- install/upgrade/repair/rollback/uninstall apply lifecycle execution;
- broad active-repo apply.

These remain behind AIDE core apply safety, review gates, explicit authorization, and capability reality updates.
