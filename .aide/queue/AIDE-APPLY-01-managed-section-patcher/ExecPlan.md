# AIDE-APPLY-01 ExecPlan

## Purpose

Implement the first reusable managed-section patcher layer for AIDE. The layer must parse explicit generated-section markers, plan fixture-only replacements, preserve manual text outside markers, detect ambiguous markers, produce transaction-compatible records, and expose report-only AIDE Lite commands.

## Scope

Allowed writes are limited to the AIDE-APPLY-01 queue packet, managed-section policies, schemas, examples, reports, AIDE Lite command/test/golden-task support, reference docs, and the new `core/apply` managed-section module.

## Non-Goals

- No active repository managed-section apply command.
- No install, upgrade, repair, rollback, or uninstall apply.
- No target repository mutation.
- No branch, worktree, merge, push, promotion, tag, release, GitHub API, provider/model, network, or Gateway behavior.
- No promotion of local `tmp/**` archive files.

## Current Facts

- Repo root: `C:/Projects/AIDE/aide`.
- HEAD before implementation: `5dcdf58c591fe1c01aa049f702e2cb5222cf9293`.
- `AIDE-REVIEW-APPLY-00` result: `PASS_WITH_WARNINGS`.
- AIDE-APPLY-01 readiness: `READY_FOR_AIDE_APPLY_01_WITH_WARNINGS`.
- Pre-existing dirty file before this queue work: `.gitignore`.
- Local `tmp/**` archive files are ignored by that pre-existing `.gitignore` edit and are not promoted.

## Milestones

1. Inspect governing queue state, transaction model records, marker conventions, and command/test patterns.
2. Create this queue packet and record scope, status, and evidence surfaces.
3. Add managed-section marker/operation policies, schemas, examples, fixtures, and core parser/patcher.
4. Add AIDE Lite `managed-section` status, validate, fixture-plan, and fixture-verify commands.
5. Add core tests, AIDE Lite tests, golden tasks, docs, reports, and next-task packet.
6. Run validation, write evidence, set status to `needs_review`, and commit the queued change set without staging unrelated dirty files.

## Progress

- 2026-06-03: Inspected repo identity, latest task packet, queue status, AIDE-REVIEW-APPLY-00 acceptance, transaction policies, existing transaction command/test patterns, and generated marker conventions.
- 2026-06-03: Created AIDE-APPLY-01 queue packet and started implementation.
- 2026-06-03: Added managed-section marker policies, schemas, examples, fixtures, `core/apply` parser/patcher code, AIDE Lite report-only commands, tests, golden tasks, docs, reports, and export-pack inclusion.
- 2026-06-03: Committed the separate direct `.gitignore` request as `2204d99 chore(gitignore): ignore tmp scratch directory`; AIDE-APPLY-01 staging excludes that change.
- 2026-06-03: Ran py_compile, unit tests, managed-section validation, transaction validation, full golden-task eval, doctor/validate/test/selftest, review-pack, verify, export-pack/pack-status, lifecycle validators, whitespace check, and strict key-pattern scan. All substantive checks passed.
- 2026-06-03: Wrote evidence and set status to `needs_review` with `PASS_WITH_WARNINGS`.

## Recovery

If interrupted before commit, inspect `status.yaml`, `git status --short --branch`, and this plan. `.gitignore` has already been committed separately as `2204d99`; keep it out of the AIDE-APPLY-01 commit. Continue only inside the task allowlist and regenerate fixture reports using `py -3 .aide/scripts/aide_lite.py managed-section fixture-plan` and `fixture-verify`.

## Validation Intent

Run py_compile, targeted unit tests, AIDE Lite managed-section commands, transaction validation, repo validation, review-pack/verify where practical, and a targeted secret scan. Record any unsupported or failing validation honestly in evidence.

## Retrospective

AIDE-APPLY-01 delivered the first reusable managed-section patcher layer but stopped at fixture-only/report-only behavior. The next responsible step is review checkpoint `AIDE-CHECK-APPLY-01`; active apply behavior remains out of scope until a future reviewed queue item explicitly authorizes it.
