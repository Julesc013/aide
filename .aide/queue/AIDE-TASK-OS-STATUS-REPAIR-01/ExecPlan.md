# AIDE-TASK-OS-STATUS-REPAIR-01 ExecPlan

## Purpose

Repair stale Task OS current/latest-task reporting after `AIDE-APPLY-02 - Scoped Transaction Executor v0` was repaired, rechecked, and accepted with notes. The repair is limited to queue/report truth and must not implement lifecycle apply behavior.

## Live Facts

- `.aide/queue/current.toml` is absent.
- `AIDE-QUEUE-CLOSURE-02` selected `AIDE-TASK-OS-STATUS-REPAIR-01` as the next safe WorkUnit.
- `AIDE-APPLY-02-scoped-transaction-executor-v0` is accepted with notes and remains review-gated.
- `AIDE-CHECK-APPLY-02-RECHECK-01` accepted the repaired scoped executor with notes.
- The old `AIDE-CHECK-APPLY-02` checkpoint remains historical and superseded by recheck evidence.
- Current Task OS output still reports raw `AIDE-APPLY-02` as missing and still recommends the old X-OS to `AIDE-APPLY-00` sequence.

## Scope

Allowed writes are limited to:

- `.aide/queue/AIDE-TASK-OS-STATUS-REPAIR-01/**`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_x_os_01_task_os_commands.py`
- `.aide/reports/task-os-*`
- `README.md`

No other files are authorized by this task. Generated non-Task-OS report churn from required status commands must be classified and not used to widen scope.

## Repair Steps

1. Create queue task metadata, status, prompt, diagnosis evidence, and allowed-path packet.
2. Patch Task OS next-selection logic so post-`AIDE-APPLY-02` accepted-with-notes state selects this repair while it is open and selects `AIDE-APPLY-LIFECYCLE-PLAN-01` as planning-only after repair.
3. Patch Task OS context/report rendering so reports distinguish:
   - absent `.aide/queue/current.toml`;
   - current task if present;
   - latest indexed queue task;
   - latest task packet raw/id/status;
   - selected next WorkUnit;
   - historical and superseded queue tasks.
4. Update the latest task packet to name this exact task ID, avoiding ambiguous shorthand.
5. Update README next-work truth to stop naming stale Q49 work as the current AIDE-local next step.
6. Add targeted Task OS tests covering post-apply accepted-with-notes selection and report distinctions.
7. Refresh Task OS generated reports.
8. Write validation, boundary, changed-files, and remaining-risk evidence.
9. Commit after validation if checks pass or warnings are classified, then stop at `needs_review`.

## Non-Goals

- No scoped transaction executor implementation.
- No lifecycle apply planning execution.
- No install apply.
- No upgrade apply.
- No repair apply.
- No rollback/uninstall apply.
- No target repo mutation.
- No branch/worktree mutation.
- No merge, push, promotion, tag, or release publication.
- No GitHub mutation.
- No provider/model calls.
- No Gateway calls.
- No network calls.
- No broad active-repo apply, broad delete, or broad move behavior.
- No production-ready or release-ready capability claim.

## Recovery

If interrupted, inspect `status.yaml`, `evidence/diagnosis.md`, `evidence/validation.md`, generated `.aide/reports/task-os-*` reports, and `git status --short --branch`. Continue only inside the allowed paths above and preserve unrelated generated report churn classifications.

## Review Gate

End at `needs_review`. This task may recommend `AIDE-APPLY-LIFECYCLE-PLAN-01` as the next planning-only WorkUnit, but it must not authorize lifecycle apply execution.
