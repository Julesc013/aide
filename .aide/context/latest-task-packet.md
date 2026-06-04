# AIDE Latest Task Packet

## PHASE

AIDE-TASK-OS-STATUS-REPAIR-01 - Task OS Current and Latest-Task Reporting Repair

## GOAL

Repair stale Task OS current/latest-task reporting after `AIDE-APPLY-02 - Scoped Transaction Executor v0` was accepted with notes, so live generated reports distinguish absent `.aide/queue/current.toml`, latest indexed queue task, latest task packet, selected next WorkUnit, historical tasks, and superseded tasks.

## WHY

`AIDE-QUEUE-CLOSURE-02` selected this repair because Task OS still reported raw `AIDE-APPLY-02` as a missing latest task and README/latest-packet guidance still pointed at stale work. Lifecycle planning must not become the next runnable WorkUnit until Task OS status truth is repaired.

## CONTEXT_REFS

- `.aide/queue/AIDE-TASK-OS-STATUS-REPAIR-01/`
- `.aide/queue/AIDE-QUEUE-CLOSURE-02/`
- `.aide/queue/AIDE-APPLY-02-scoped-transaction-executor-v0/`
- `.aide/queue/AIDE-APPLY-02-REPAIR-01/`
- `.aide/queue/AIDE-CHECK-APPLY-02-RECHECK-01/`
- `.aide/reports/task-os-task-status.md`
- `.aide/reports/task-os-command-status.md`
- `.aide/reports/task-os-next-plan.md`

## ALLOWED_PATHS

- `.aide/queue/AIDE-TASK-OS-STATUS-REPAIR-01/**`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_x_os_01_task_os_commands.py`
- `.aide/reports/task-os-*`
- `README.md`

## FORBIDDEN_PATHS

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
- scoped transaction executor implementation files outside Task OS reporting
- managed-section implementation files
- install/upgrade/repair/rollback/uninstall implementation files
- unrelated contracts, schemas, governance, and docs/reference files

## IMPLEMENTATION

- Repair Task OS status/report truth only.
- Do not implement scoped transaction executor behavior.
- Do not implement lifecycle apply planning execution.
- Recommend `AIDE-APPLY-LIFECYCLE-PLAN-01` only as a future planning-only WorkUnit after this repair is review-gated.

## EVIDENCE

- `.aide/queue/AIDE-TASK-OS-STATUS-REPAIR-01/evidence/diagnosis.md`
- `.aide/queue/AIDE-TASK-OS-STATUS-REPAIR-01/evidence/changed-files.md`
- `.aide/queue/AIDE-TASK-OS-STATUS-REPAIR-01/evidence/repair-summary.md`
- `.aide/queue/AIDE-TASK-OS-STATUS-REPAIR-01/evidence/validation.md`
- `.aide/queue/AIDE-TASK-OS-STATUS-REPAIR-01/evidence/boundary-confirmation.md`
- `.aide/queue/AIDE-TASK-OS-STATUS-REPAIR-01/evidence/remaining-risks.md`

## NON_GOALS

- No scoped transaction executor implementation.
- No lifecycle apply execution.
- No install apply.
- No upgrade apply.
- No repair apply.
- No rollback/uninstall apply.
- No target repository mutation.
- No branch/worktree mutation, merge, push, promotion, tag, or release publication.
- No GitHub mutation.
- No provider/model calls.
- No Gateway calls.
- No network calls.
- No broad active-repo apply, broad delete, or broad move behavior.
- No production-ready or release-ready claim.

## VALIDATION

- `git status --short --branch`
- `git diff --check`
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_x_os_01_task_os_commands.py`
- `py -3 .aide/scripts/aide_lite.py task status`
- `py -3 .aide/scripts/aide_lite.py task classify`
- `py -3 .aide/scripts/aide_lite.py task next-plan`
- `py -3 .aide/scripts/aide_lite.py validate`
- boundary text searches
- changed-file secret scan
- `py -3 .aide/scripts/aide_lite.py commit check --latest`

## ACCEPTANCE

- Task OS status reports do not report stale raw `AIDE-APPLY-02` as a missing latest/current task.
- Reports distinguish absent current.toml, latest indexed task, latest task packet, selected next WorkUnit, historical tasks, and superseded tasks.
- README next-work truth is no longer stale.
- `AIDE-APPLY-LIFECYCLE-PLAN-01` is planning-only and does not authorize lifecycle apply execution.
- Status ends at `needs_review`.

## OUTPUT_SCHEMA

Return `STATUS`, `SUMMARY`, `FILES CHANGED`, `LIVE REPO STATE`, `VALIDATION`, `WARNINGS`, `RISKS`, `FORBIDDEN OPERATIONS PRESERVED`, and `NEXT TASK`.

## TOKEN_ESTIMATE

- method: chars / 4, rounded up
- approx_tokens: 1150
- budget_status: PASS
