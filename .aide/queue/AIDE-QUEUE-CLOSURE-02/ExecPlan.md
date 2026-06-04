# AIDE-QUEUE-CLOSURE-02 ExecPlan

## Purpose

Rerank the remaining AIDE queue blockers now that `AIDE-APPLY-02 - Scoped Transaction Executor v0` has been repaired, rechecked, and accepted with notes. This task treats blockers, prerequisites, prohibitions, failures, partials, stale evidence, missing authority, and incomplete reviews as first-class graph states, then selects the smallest safe next WorkUnit batch.

## Scope

Allowed writes are limited to `.aide/queue/AIDE-QUEUE-CLOSURE-02/**`, `.aide/queue/index.yaml`, and generated report files refreshed by required report-only AIDE status commands. This task may inspect queue files, status files, evidence, generated reports, capability reality reports, validation output, and apply/check artifacts.

## Non-Goals

- No implementation file mutation.
- No scoped transaction executor implementation.
- No lifecycle apply planning execution.
- No install apply.
- No upgrade apply.
- No lifecycle repair apply.
- No rollback/uninstall apply.
- No target repo mutation.
- No branch/worktree mutation.
- No merge, push, promotion, tag, release publication, or GitHub mutation.
- No provider/model calls.
- No Gateway calls.
- No network calls.
- No broad active-repo apply, delete, or move behavior.
- No production-ready or release-ready capability claim.

## Current Facts

- Repo root: `C:/Projects/AIDE/aide`.
- HEAD at start: `ce7e04a303553058013c4eabb5648f72b311e1e5`.
- Branch status at start after required status-command refresh: `main...origin/main` with generated report churn.
- `git rev-list --left-right --count origin/main...HEAD`: `0 0`.
- `.aide/queue/current.toml`: absent.
- `AIDE-APPLY-02-scoped-transaction-executor-v0`: `needs_review`, `planning_state=accepted_with_notes`.
- `AIDE-CHECK-APPLY-02`: historical `NEEDS_REPAIR`, superseded by recheck evidence.
- `AIDE-APPLY-02-REPAIR-01`: `needs_review`, `planning_state=accepted_with_notes`.
- `AIDE-CHECK-APPLY-02-RECHECK-01`: `needs_review`, `recheck_disposition=ACCEPTED_WITH_NOTES`.
- `task status` still reports `latest_task_id: AIDE-APPLY-02` and `latest_task_status: missing`.
- `.aide/context/latest-task-packet.md` still describes the older AIDE-APPLY-02 setup context and allowed paths.
- `README.md` still names Q49 as next AIDE-local work.

## Milestones

1. Run preflight commands and classify generated report churn.
2. Inspect AIDE-QUEUE-CLOSURE-01 and the AIDE-APPLY-02, CHECK, REPAIR, and RECHECK chain.
3. Rebuild a compact graph from live repo truth.
4. Reconcile accepted-with-notes and superseded states without erasing history.
5. Apply the lifecycle planning gate and select exactly one next WorkUnit batch.
6. Write closure artifacts and evidence.
7. Run validation, boundary searches, machine-readable checks, and secret scan.
8. Commit if validation passes or warnings are classified, then stop at review.

## Selected Next Batch

Exactly one task is selected for future execution:

```text
AIDE-TASK-OS-STATUS-REPAIR-01
```

The selected task is not executed here. It should repair stale Task OS current/latest-task reporting and stale generated guidance before lifecycle planning is promoted to the next runnable WorkUnit.

## Apply Lifecycle Planning Gate

`AIDE-APPLY-LIFECYCLE-PLAN-01` may be proposed later because AIDE-APPLY-02 is accepted with notes, but it remains blocked in this closure pass by stale current-task and Task OS status truth. Lifecycle planning must remain planning-only and must not authorize lifecycle apply, install apply, upgrade apply, lifecycle repair apply, rollback/uninstall apply, target repo mutation, branch/worktree mutation, merge, push, promotion, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, or broad active-repo apply.

## Recovery

If interrupted, inspect `status.yaml`, `blocker-graph.md`, `blocker-graph.json`, `closure-plan.md`, `next-batch.md`, and `evidence/validation.md`. Re-run required status commands, keep edits inside this task allowlist, and continue only if no unrelated user changes would be overwritten.

## Validation Intent

Run `git status --short --branch`, `git diff --check`, `task status`, `validate`, `scoped-transaction status`, `managed-section status`, `transaction status`, task inspect/evidence commands, JSON parsing, YAML fallback checks, boundary text searches, changed-file secret scan, and `commit check --latest` after committing.

## Retrospective

This task intentionally selects a repair/report WorkUnit as the next safe batch. It does not execute the repair, implement lifecycle planning, or widen any apply capability.
