# X-OS-00 ExecPlan

## Purpose

Define the first AIDE Task OS foundation layer as report-only policy, schemas, examples, docs, tests, golden tasks, validation registration, export-pack sync, and queue evidence.

## Scope

This task is limited to Task OS v0 contracts: WorkUnit, TaskAttempt, Blocker, RepairTask, Wave, Checkpoint, BranchProvenance, CapabilityReality, and append-only ledger records. It may update AIDE Lite validation only to check presence, JSON shape, examples, golden catalog entries, and no-apply anchors.

## Non-Goals

- No Task OS scheduling.
- No active repair loop.
- No branch creation, worktree creation, merge, push, prune, promotion, or checkpoint apply.
- No install, repair, upgrade, rollback, uninstall, or transactional apply.
- No target-repo work, target tests, target sync, provider/model calls, network calls, GitHub API mutation, tags, uploads, or release publication.

## Allowed Paths

The allowlist is the one recorded in `task.yaml`. Do not widen it without a new reviewed task.

## Facts Verified

- Current repo root is `C:/Projects/AIDE/aide`.
- `origin` points at `https://github.com/Julesc013/aide.git`.
- Current baseline commit before X-OS-00 edits is `91da3fab9f61a02dc044fec8f3348bd24eee9789`.
- AIDE-CONTINUE-00 exists, is committed, and classifies `X-TEST-01` as `DEFERRED_TARGET_WORK`.
- Latest task packet points to X-OS-00.
- X-TEST-00 exists, is implemented, and remains `needs_review`.
- Target work and apply/promotion automation remain gated.

## Milestones

- [x] Inspect repo identity, queue preconditions, X-TEST-00, AIDE-CONTINUE-00, and overlapping policies.
- [x] Create X-OS-00 queue packet and initial ExecPlan.
- [x] Add Task OS policies, schemas, ledgers, examples, and docs.
- [x] Add golden tasks, tests, and minimal validation registration.
- [x] Refresh export pack and latest task packet for X-OS-01.
- [x] Run validation and record evidence.
- [ ] Commit structured X-OS-00 changes.

## Validation Intent

Run the required AIDE validation suite from the prompt, including doctor, validate, test, selftest, eval run, pack-status, release and lifecycle validators, canonical unittest discovery for `.aide/scripts/tests`, diff check, commit check, and a targeted secret scan. Unsupported commands must be recorded as unsupported, not passed.

## Recovery

This task is restartable from this ExecPlan and `status.yaml`. If interrupted, inspect `git status --short --branch`, this packet, and `evidence/` before editing. If validation fails, fix only inside allowed paths or record a blocker. Do not mutate branches or target repos to recover.

## Retrospective

X-OS-00 completed the policy, schema, example, docs, golden-task, validation, and export-pack contract layer and stopped at `needs_review`. Validation passed with expected non-blocking warnings only: review gate, dirty-source pack provenance before commit, generated report refresh, and X-OS-01 handoff. No `task-os` command group, worker execution, branch mutation, target mutation, provider/model/network call, release publication, merge, push, promotion, or apply behavior was introduced.
