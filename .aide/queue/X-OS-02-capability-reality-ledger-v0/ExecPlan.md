# X-OS-02 ExecPlan

## Purpose

Implement a no-call, report-only capability reality ledger layer over the Task OS schema, policy, and command foundation.

## Scope

This task adds controlled capability seeds, observation and overclaim schemas, generated capability reports, AIDE Lite `capability` commands, validation hooks, tests, golden tasks, export-pack inclusion, and reference documentation. Commands may inspect repo-local policies, docs, tests, golden tasks, reports, queue records, and AIDE Lite source and may write generated reports under `.aide/reports/capability-*`.

## Non-Goals

- No Task OS scheduler, worker, or autonomous loop.
- No task execution.
- No repair execution or repair apply.
- No install, repair, upgrade, rollback, uninstall, or transactional apply.
- No branch creation, worktree creation, merge, push, prune, promotion, or checkpoint apply.
- No target-repo work, target sync, target tests, provider/model calls, network calls, GitHub API mutation, tags, uploads, or release publication.
- No Runtime, Hosts, Commander, Mobile, Gateway, provider, MCP/A2A, UI, or app-surface implementation.

## Allowed Paths

The allowlist is the one recorded in `task.yaml`. Do not widen it without a new reviewed task.

## Facts Verified

- Current repo root is `C:/Projects/AIDE/aide`.
- Current baseline commit before X-OS-02 edits is `11e30cb7c6ae94e7fb3b9541b9bd2ffca1da5ec8`.
- Worktree was clean at start.
- X-OS-00 and X-OS-01 exist, are committed, and are `needs_review` with `PASS_WITH_WARNINGS` evidence.
- Latest task packet initially pointed to X-OS-02.
- Apply, branch/worktree, promotion, release, provider/model/network, target, task execution, and repair execution remain gated.

## Milestones

- [x] Inspect repo identity, queue preconditions, capability policy/schema, X-OS-01 report-command patterns, and validation hooks.
- [x] Create X-OS-02 queue packet and initial ExecPlan.
- [x] Add capability seed records, schemas, and capability reality policy updates.
- [x] Add report-only AIDE Lite capability command builders and parser registrations.
- [x] Generate capability command status, observations, ledger, overclaim, and validation reports.
- [x] Add tests, golden tasks, docs, validation registration, and export-pack sync.
- [x] Generate latest task packet for AIDE-CHECK-OS-01.
- [x] Run validation and record evidence.
- [ ] Commit structured X-OS-02 changes.

## Validation Intent

Run the required AIDE validation suite from the prompt, including doctor, validate, test, selftest, eval run, all new capability commands, pack-status, verifier/review-pack, harness validation, canonical unittest discovery for `.aide/scripts/tests`, diff check, commit check, and a targeted secret scan. Unsupported commands must be recorded as unsupported, not passed.

## Recovery

This task is restartable from this ExecPlan and `status.yaml`. If interrupted, inspect `git status --short --branch`, this packet, generated reports, and `evidence/` before editing. If validation fails, fix only inside allowed paths or record a blocker. Do not mutate branches or target repos to recover.

## Retrospective

X-OS-02 implemented the report-only capability reality layer and generated the required `.aide/reports/capability-*` outputs. Validation passed with expected warnings only: review gate required, dirty export-pack provenance before commit, stale root generated-manifest warning, route token-budget advisory, and one non-blocking overclaim wording review.
