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

## 2026-09-29 stale next-work repair

Objective: stop the self-hosted Task OS from recommending the historical
`AIDE-APPLY-LIFECYCLE-PLAN-01` as a new runnable task once its queue status is
already `needs_review` or otherwise complete. The read-only selector on clean
`dev@0d9741e3` currently does so even though later lifecycle source and
current-ZIP consumers have progressed. Keep this old phase selector honest;
do not invent a current campaign priority or weaken review gates.

Scope: this WorkUnit, `.aide/scripts/aide_lite.py`, and its focused Task OS
test. Add a red regression with a completed lifecycle-plan item, then return
an explicit current-queue review fallback with lifecycle-plan readiness false.
Preserve the old planning recommendation when that item is genuinely absent or
pending. Run focused tests and source validation; obtain independent changed
scope review before dev integration. Keep the frozen release ZIP unchanged and
route any changed-byte projection through the existing release WorkUnit.

The new fixture failed red: an already `needs_review` lifecycle plan was
selected again. After the source repair, 11/11 X-OS-01 tests and 9/9 X-OS-00
tests passed with process-local temporary files under the approved D scratch
root. Python AST and `git diff --check` passed; `git status` showed only this
plan, the intended source and test. A read-only selection on the actual AIDE
queue now says `Review current AIDE queue WorkUnits`, gives the historical
`needs_review` reason, and reports lifecycle-plan readiness false. This does
not infer the next campaign priority or authorize lifecycle apply. Freeze the
source subject for independent review before any dev or release projection.

## 2026-09-29 non-mutating next-plan inspection

Objective: make `task next-plan` inspection read-only by default, consistent
with `task status`, while preserving explicit generation of its tracked report.
The current command writes `.aide/reports/task-os-next-plan.md` even for a
simple queue query; the tracked snapshot is already older than the current
selector. This causes avoidable report churn and can confuse snapshot truth
with live queue truth.

Scope: this WorkUnit, the existing CLI handler/parser, and focused Task OS
tests. Add a regression showing the default command leaves a sentinel report
unchanged and an explicit `--write-report` refreshes it. Preserve the direct
report writer and its other callers. Run the focused suite with process-local
D scratch, read-only check on the actual queue, source checks and independent
changed-scope review before dev integration. Keep release bytes frozen until
the coherent current-source release projection.

The new 12-case suite failed red because the parser had no `write_report`
option. After the CLI repair, X-OS-01 passed 12/12 and X-OS-00 passed 9/9 with
process-local D scratch. AST and `git diff --check` passed. An actual
`task next-plan` query returned the live current-queue review fallback while
the tracked report hash stayed unchanged. The initial X-OS-00 command used an
incorrect file pattern and ran zero tests; the corrected command passed 9/9.
Keep the tracked report as an older snapshot until an explicit release
projection; do not claim that inspection regenerated it.
