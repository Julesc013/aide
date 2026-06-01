# X-OS-01 ExecPlan

## Purpose

Implement the first no-call, report-only Task OS command layer over the X-OS-00 schema and policy contracts.

## Scope

This task adds deterministic AIDE Lite commands for task status/classification, repair/requeue/resume plans, blocker status/classification, wave status/plan, and checkpoint status/plan. Commands may inspect repo-local queue, context, policy, evidence, and report files and may write generated reports under `.aide/reports/task-os-*`.

## Non-Goals

- No Task OS scheduler or autonomous loop.
- No task execution.
- No repair execution or repair apply.
- No install, repair, upgrade, rollback, uninstall, or transactional apply.
- No branch creation, worktree creation, merge, push, prune, promotion, or checkpoint apply.
- No target-repo work, target sync, target tests, provider/model calls, network calls, GitHub API mutation, tags, uploads, or release publication.

## Allowed Paths

The allowlist is the one recorded in `task.yaml`. Do not widen it without a new reviewed task.

## Facts Verified

- Current repo root is `C:/Projects/AIDE/aide`.
- `origin` points at `https://github.com/Julesc013/aide.git`.
- Current baseline commit before X-OS-01 edits is `1828a46485a2f0f538c4a699f6a5d00019a78aad`.
- Worktree was clean at start.
- AIDE-CONTINUE-00 exists, is committed, and classifies `X-TEST-01` as `DEFERRED_TARGET_WORK`.
- X-OS-00 exists, is committed, and is `needs_review` with `PASS_WITH_WARNINGS` evidence.
- Latest task packet initially pointed to X-OS-01; final handoff packet points to X-OS-02.
- Apply, branch/worktree, promotion, release, provider/model/network, target, and repair execution remain gated.

## Milestones

- [x] Inspect repo identity, queue preconditions, X-OS-00, policies, parser patterns, and existing reports.
- [x] Create X-OS-01 queue packet and initial ExecPlan.
- [x] Add report-only Task OS command builders and parser registrations.
- [x] Generate Task OS command reports.
- [x] Add tests, golden tasks, docs, validation registration, and export-pack sync.
- [x] Generate latest task packet for X-OS-02.
- [x] Run validation and record evidence.
- [ ] Commit structured X-OS-01 changes.

## Validation Intent

Run the required AIDE validation suite from the prompt, including doctor, validate, test, selftest, eval run, all new Task OS commands, pack-status, verifier/review-pack, harness validation, canonical unittest discovery for `.aide/scripts/tests`, diff check, commit check, and a targeted secret scan. Unsupported commands must be recorded as unsupported, not passed.

## Recovery

This task is restartable from this ExecPlan and `status.yaml`. If interrupted, inspect `git status --short --branch`, this packet, generated reports, and `evidence/` before editing. If validation fails, fix only inside allowed paths or record a blocker. Do not mutate branches or target repos to recover.

## Retrospective

X-OS-01 implemented the report-only command layer and generated the required `.aide/reports/task-os-*` outputs. Validation passed with expected warnings only: review gate required, dirty export-pack provenance before commit, assigned X-OS-02 next packet, and the pre-existing root harness generated-manifest stale warning.
