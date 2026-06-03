# AIDE-CHECK-APPLY-01 ExecPlan

## Purpose

Review AIDE-APPLY-01 before any scoped transaction executor or install/upgrade/repair/rollback/uninstall apply phase starts.

## Scope

- Inspect AIDE-APPLY-01 queue status, evidence, policies, schemas, examples, implementation, docs, tests, reports, golden tasks, and export-pack state.
- Classify managed-section patcher readiness and AIDE-APPLY-02 readiness.
- Record no-real-apply, no-target, no-branch, no-release, no-provider, and no-network boundaries.
- Write checkpoint reports, warning disposition, validation evidence, and the next-task packet.

## Non-Goals

- No AIDE-APPLY-02 implementation.
- No active repository managed-section or transaction apply command.
- No target repository mutation.
- No install, repair, upgrade, rollback, or uninstall apply behavior.
- No branch/worktree mutation, merge, push, promotion, tag, release publication, GitHub API mutation, provider/model call, network call, or Gateway forwarding.

## Allowed Paths

Allowed paths are the queue packet, top-level checkpoint reports, latest task/review packets, and deterministic validation/report artifacts listed in `task.yaml`.

## Milestones

1. Inspect repository identity, branch state, AIDE-APPLY-01 status, and preconditions.
2. Audit managed-section policies, schemas, examples, implementation, docs, tests, golden tasks, and reports.
3. Record manual-content preservation, conflict detection, rollback evidence, command surface, export-pack/release boundary, and AIDE-APPLY-02 readiness.
4. Run the validation matrix and classify warnings.
5. Commit scoped checkpoint artifacts and run commit policy validation.

## Validation Intent

Use existing AIDE validation commands plus targeted unit tests, `git diff --check`, `git check-ignore tmp/`, and a targeted secret scan. Unsupported commands must be recorded honestly.

## Evidence

Evidence is recorded under `evidence/` and in the top-level checkpoint reports. The final status remains `needs_review`.
