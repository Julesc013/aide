# AIDE-QUEUE-CLOSURE-02 Next Batch

## Selected Batch

Exactly one future WorkUnit:

```text
AIDE-TASK-OS-STATUS-REPAIR-01
```

## Goal

Repair stale Task OS current/latest-task reporting and related current-task guidance after `AIDE-APPLY-02` was accepted with notes.

## Why Selected

- `AIDE-APPLY-02-scoped-transaction-executor-v0` is accepted with notes.
- Historical `AIDE-CHECK-APPLY-02` NEEDS_REPAIR is superseded by `AIDE-CHECK-APPLY-02-RECHECK-01`.
- `py -3 .aide/scripts/aide_lite.py validate` passes.
- `py -3 .aide/scripts/aide_lite.py task status` still reports `latest_task_id: AIDE-APPLY-02` with status `missing`.
- `.aide/context/latest-task-packet.md` still describes the old AIDE-APPLY-02 setup context.
- `README.md` still names Q49 as next AIDE-local work.
- Those stale status surfaces affect current-task truth and outrank apply lifecycle planning under the prompt priority order.

## Blockers Resolved

- stale Task OS latest-task selector;
- stale latest-task packet;
- stale generated Task OS next recommendation;
- stale next-work guidance if explicitly allowed;
- lifecycle planning gate blocker caused by unreliable current-task truth.

## Proposed Allowed Paths

- `.aide/queue/AIDE-TASK-OS-STATUS-REPAIR-01/**`
- `.aide/context/latest-task-packet.md`
- `.aide/reports/task-os-*.md`
- `.aide/reports/task-os-*.json`
- `.aide/queue/index.yaml`
- `README.md` only if the repair task explicitly authorizes docs normalization

## Proposed Protected Paths

- `.git/**`
- `.github/**`
- `.aide.local/**`
- `.env`
- `.env.*`
- `secrets/**`
- `credentials/**`
- target repositories
- release publication files
- provider/model/Gateway integration files
- branch/worktree automation files
- implementation files outside the repair task

## Forbidden Operations

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
- production-ready overclaim
- release-ready overclaim

## Validation

- `git status --short --branch`
- `git diff --check`
- `py -3 .aide/scripts/aide_lite.py task status`
- `py -3 .aide/scripts/aide_lite.py validate`
- targeted Task OS status/current command checks
- parse checks for changed JSON/YAML files
- boundary searches over changed repair artifacts
- changed-file secret scan

## Expected Evidence

- task-local changed files list;
- before/after Task OS status evidence;
- stale latest-task packet disposition;
- allowed paths and protected paths confirmation;
- forbidden operations confirmation;
- validation command log;
- remaining risks;
- review gate status.

## Why Safe Now

The task is report/status repair only. It does not widen apply authority, does not modify executor behavior, does not mutate target repositories, does not mutate branch/worktree state, does not use network/provider/Gateway/GitHub operations, and does not execute lifecycle apply planning. It removes a current-task truth blocker before any broader planning proceeds.

## Prompt Seed

Task ID: `AIDE-TASK-OS-STATUS-REPAIR-01`

Repair stale Task OS current/latest-task reporting after `AIDE-APPLY-02-scoped-transaction-executor-v0` was accepted with notes by `AIDE-CHECK-APPLY-02-RECHECK-01`. Create or use a live queue task with an ExecPlan, explicit allowed paths, protected paths, forbidden operations, validation, evidence, and review gate. Scope the work to Task OS status/current-task truth and generated task report surfaces. Do not implement lifecycle apply planning, do not mutate implementation files, target repos, branches, worktrees, releases, GitHub, providers/models, Gateway, or network, and do not perform install apply, upgrade apply, lifecycle repair apply, rollback/uninstall apply, or broad active-repo apply. End at `needs_review`.
