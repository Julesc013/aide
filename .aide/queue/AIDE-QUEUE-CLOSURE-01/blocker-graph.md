# AIDE-QUEUE-CLOSURE-01 Blocker Graph

## Scope

This is a report-only graph. It summarizes current queue truth, generated Task OS blocker records, stale generated guidance, missing authority, hard prohibitions, and the next safe WorkUnit. It does not repair or execute any blocker.

## Live Inputs

- `git status --short --branch`: `main...origin/main [ahead 1]`.
- `git rev-parse HEAD`: `50295a038b80e50ee9afe62ec55ebb7721ab4be8`.
- `.aide/queue/current.toml`: absent.
- `.aide/queue/index.yaml`: 69 indexed tasks.
- `task status`: latest task resolves to `AIDE-APPLY-02-scoped-transaction-executor-v0`.
- `task current`: still reports `AIDE-CHECK-APPLY-01-managed-section-patcher-review`.
- `managed-section status`: PASS, report-only, real apply false.
- `transaction status`: PASS, report-only, real apply false.
- `doctor`: PASS.
- `validate`: PASS.
- `verify`: PASS.
- `blocker status`: 42 blocker records; 1 repairable, 41 non-repairable.
- `capability ledger`: PASS, 13 records; one `unknown` capability remains.

## Graph Counts

- modeled_nodes: 98
- modeled_edges: 127

## Node Groups

- queue_task: 69
- task_os_blocker_or_deferral: 4 target deferral nodes plus review-gated state reflected through queue tasks
- legacy_unindexed_queue_dir: 3
- prohibited_operation: 15
- stale_report_or_command_surface: 4
- missing_authority_or_future_capability: 1
- unclear_capability_reality: 1
- human_decision: 1

## State Counts

- READY: 1
- PARTIAL: 3
- FAILED_VALIDATION: 0
- BLOCKED_MISSING_AUTHORITY: 1
- BLOCKED_MISSING_PREREQUISITE: 4
- BLOCKED_ALLOWED_PATH: 0
- BLOCKED_PROTECTED_PATH: 0
- BLOCKED_PROHIBITED_OPERATION: 15
- BLOCKED_DIRTY_WORKTREE: 0
- BLOCKED_REMOTE_DIVERGENCE: 0
- BLOCKED_MISSING_EVIDENCE: 0
- BLOCKED_REVIEW_REQUIRED: 30
- BLOCKED_UNCLEAR_QUEUE_STATE: 1
- BLOCKED_UNCLEAR_CAPABILITY_REALITY: 1
- STALE_EVIDENCE: 4
- SUPERSEDED: 0
- DUPLICATE: 0
- NEEDS_HUMAN_DECISION: 1
- DONE: 38

## Queue Task State

- DONE: 38 indexed tasks have `status=passed`.
- BLOCKED_REVIEW_REQUIRED: 30 indexed tasks have `status=needs_review`.
- READY: 1 indexed task, `AIDE-APPLY-02-scoped-transaction-executor-v0`, has `status=pending` and `planning_state=authorized_for_implementation`.

## Partial Or Unindexed Queue Directories

The following queue directories exist but do not follow the standard task packet shape and are not indexed tasks:

- `foundation-review`
- `full-audit`
- `post-q08-foundation-review`

They are classified as PARTIAL historical/review records, not current executable WorkUnits.

## Stale Or Lagging Surfaces

- `task current` reports `AIDE-CHECK-APPLY-01-managed-section-patcher-review`, while `task status` resolves latest to `AIDE-APPLY-02-scoped-transaction-executor-v0`.
- `.aide/context/latest-task-packet.md` still names generic `AIDE-APPLY-02 - Scoped Transaction Executor v0`; it does not yet point to the exact queue id created by the authorization task.
- `wave status` still describes the older Task OS foundation wave with X-OS-02 planned/deferred language.
- `wave plan` and `checkpoint status` still suggest the older X-OS to AIDE-APPLY-00 sequence, even though AIDE-APPLY-00, AIDE-APPLY-01, and AIDE-APPLY-02 authorization now exist in the live queue.

These are STALE_EVIDENCE or BLOCKED_UNCLEAR_QUEUE_STATE nodes. They should not override `.aide/queue/index.yaml` and live task packets.

## Hard Prohibition Nodes

The following remain BLOCKED_PROHIBITED_OPERATION unless a future reviewed queue task explicitly changes authority:

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

## Top Blockers

### AIDE-APPLY-02 Implementation Not Started

- state: READY
- source: `.aide/queue/AIDE-APPLY-02-scoped-transaction-executor-v0/status.yaml`
- why it blocks progress: AIDE-CHECK-APPLY-02 and lifecycle planning cannot proceed until the scoped executor is implemented.
- unblock path: run `AIDE-APPLY-02-IMPLEMENT` inside the existing allowlist and end at review.

### Review-Gated Work Backlog

- state: BLOCKED_REVIEW_REQUIRED
- source: `.aide/queue/index.yaml`, `blocker status`
- why it blocks progress: 30 tasks are implemented or checkpointed but remain `needs_review`.
- unblock path: review gates must be resolved by explicit review/checkpoint tasks; do not self-promote.

### Stale Task OS Guidance

- state: STALE_EVIDENCE / BLOCKED_UNCLEAR_QUEUE_STATE
- source: `task current`, `wave status`, `wave plan`, `checkpoint status`
- why it blocks progress: generated report surfaces lag behind the live apply queue and can misroute future workers.
- unblock path: after AIDE-APPLY-02 implementation/checkpoint, create a narrow Task OS status-current repair if still stale.

### Target Deferrals

- state: BLOCKED_MISSING_PREREQUISITE
- source: `task-os-blocker-status.md`
- why it blocks progress: target repo work is intentionally deferred until AIDE core apply and validation state permits it.
- unblock path: do not execute now; revisit only after explicit target-work authorization.

### Queue Closure As Core Automation

- state: BLOCKED_MISSING_AUTHORITY
- source: current user request plus live queue policy
- why it blocks progress: report-only closure planning is authorized now; implementation of a reusable closure command surface is not yet authorized.
- unblock path: after AIDE-CHECK-APPLY-02, create `AIDE-QUEUE-CLOSURE-02` for implementation if review supports it.

### Unknown Capability Reality

- state: BLOCKED_UNCLEAR_CAPABILITY_REALITY
- source: `.aide/reports/capability-ledger.md`
- why it blocks progress: `autonomous_task_scheduler` remains `unknown`, and closure must not become unbounded autonomy.
- unblock path: keep queue closure report-only until a reviewed task defines precise command boundaries.
