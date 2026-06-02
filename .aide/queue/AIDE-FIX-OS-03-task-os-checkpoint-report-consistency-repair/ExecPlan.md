# AIDE-FIX-OS-03 ExecPlan

## Purpose

Repair stale report-only Task OS readiness outputs found by AIDE-CHECK-OS-01 so AIDE can trust its generated checkpoint and next-plan reports before any AIDE-APPLY-00 work begins.

## Scope

This task may update the AIDE Lite report-generation logic, focused Task OS command tests, one golden acceptance note, queue-local evidence, generated Task OS reports, generated capability reports refreshed by required golden validation, generated task packet, and validation/review artifacts listed in `task.yaml`.

## Non-Goals

- No AIDE-APPLY-00 implementation.
- No transactional apply, install apply, repair apply, upgrade apply, rollback apply, uninstall apply, or checkpoint apply.
- No target repository mutation, branch/worktree mutation, merge, push, promotion, release publication, tag creation, GitHub API mutation, provider/model/network call, Gateway forwarding, task execution scheduler, or repair execution.

## Allowed Paths

The allowlist is recorded in `task.yaml`. Do not widen it except to capture deterministic generated outputs from required validation commands.

## Facts Verified

- Starting HEAD for this repair is `d36bdd12f101098c3a268beabe229c565806447c`.
- `AIDE-CHECK-OS-01` ended at `needs_review` with `PARTIAL_NEEDS_REPAIR`.
- Preflight `doctor` and `validate` passed.
- Preflight `task status` reproduced the latest-task parsing bug as `latest_task_id: X-OS-03`.
- Preflight `git plan` was report-only and blocked on the expected dirty tree after generated reports were refreshed.

## Milestones

- [x] Read governing queue, source-of-truth, review-gate, and latest task packet records.
- [x] Create bounded queue packet and restartable ExecPlan.
- [x] Repair latest-task parsing and generated Task OS report selection logic.
- [x] Add focused tests and golden expectation updates.
- [x] Regenerate Task OS reports and latest task packet.
- [x] Run validation and write evidence.
- [x] Commit structured repair and run commit check.

## Result

- Latest-task parsing now preserves `AIDE-FIX-OS-03` and resolves it to `AIDE-FIX-OS-03-task-os-checkpoint-report-consistency-repair`.
- Checkpoint status reports `x_os_02_status: needs_review` from queue truth and no longer hardcodes `missing_or_not_done`.
- Command status and next-plan now select `AIDE-APPLY-00 - Transaction Model` only after X-OS-02, AIDE-CHECK-OS-01, and AIDE-FIX-OS-03 are locally complete for review.
- Latest task packet points to AIDE-APPLY-00 as a proposed next queue packet only; no apply behavior was implemented.
- Review gate remains required.

## Validation Intent

Run focused Task OS tests, AIDE Lite validation, report-only Task OS command checks, eval/golden coverage, verifier, whitespace check, targeted secret scan, and commit message check.

## Recovery

On resume, inspect `git status --short --branch`, this ExecPlan, `status.yaml`, `evidence/validation.md`, generated `.aide/reports/task-os-*` outputs, and the latest validation results. Continue with report-only repairs only; do not mutate targets, branches, releases, providers, models, network, or apply-capable surfaces.
