# Q38 ExecPlan

## Objective

Implement AIDE's first deterministic File Quality Ledger so repo quality gaps
are visible as reviewable evidence before future refactor, root recycling,
install, upgrade, repair, rollback, or release work acts on files.

## Scope

Allowed paths are the paths listed in `task.yaml`, with Q38-specific changes
kept to quality policies, `.aide/quality/**`, generated quality reports under
`.aide/reports/`, `.aide/scripts/aide_lite.py`, `.aide/scripts/tests/**`,
golden tasks, compact docs, generated Q39 context artifacts, export-pack
support, and this queue packet. Generated validation churn outside this scope
is not part of the task diff.

## Non-Goals

- Do not move, delete, rename, refactor, migrate, absorb, or rewrite files.
- Do not declare files dead; Q38 only emits warnings and candidates.
- Do not call providers, models, outbound network services, embeddings, or
  vector search.
- Do not mutate branches, push, merge, prune, tag, publish, call GitHub APIs,
  or install active workflows.
- Do not mutate Eureka, Dominium, or external repositories.
- Do not implement Q39 Refactor Control Plane v0 or later root/install phases.

## Milestones

1. Confirm Q37 repo intelligence outputs exist and record baseline validation.
2. Create the Q38 queue packet and add it to the filesystem queue index.
3. Define file quality, docs consistency, module quality, and reuse/modularity
   policies plus lightweight schemas.
4. Implement `aide_lite.py quality ledger|validate|status|explain-file|docs|tests|modules|reuse`.
5. Add deterministic unittest coverage and golden tasks.
6. Generate quality ledger JSON and compact Markdown reports.
7. Update docs, command catalog, and Q39 latest task packet references.
8. Regenerate the portable export pack and record evidence.
9. Run validation and move Q38 to `needs_review`.

## Progress

- 2026-05-14: Q37 status inspected and found implemented with `needs_review`;
  repo intelligence artifacts are present. Baseline validation found the
  committed export pack checksums invalid, which Q38 export-pack sync will
  repair within allowed scope.
- 2026-05-14: Q38 queue packet created with this restartable ExecPlan.
- 2026-05-14: File quality, docs consistency, module quality, and
  reuse/modularity policies and schemas were added.
- 2026-05-14: AIDE Lite quality commands, Q38 tests, and deterministic golden
  tasks were implemented.
- 2026-05-14: Quality ledger and summary reports were generated from Q37 repo
  intelligence. Current ledger summary: 1589 files, 297 exempt, 50 pass,
  1242 warn, 0 fail.
- 2026-05-14: Export pack regenerated with portable Q38 support and without
  source-generated quality reports as target truth. `pack-status` passes.
- 2026-05-14: Evidence completed and Q38 moved to `needs_review`.

## Decisions

- Direct edits and commits occur on `main` because the prompt requires commits
  and forbids branch mutation. Branch-policy risk is recorded rather than fixed
  by creating a task branch.
- Q38 levels are transparent labels, not opaque numeric scores.
- Warnings and candidates mean "inspect before acting"; they are not deletion
  advice or proof that a file is dead.
- Target repositories must generate their own quality ledgers after import;
  AIDE source-generated quality reports are not target truth.

## Validation Intent

Run proportionate checks: `git diff --check`, quality commands, targeted Q38
unittest discovery, AIDE Lite tests, golden tasks, Harness/Core unittest suites,
export-pack and pack-status, repo/intent validation, command catalog validation,
and a targeted secret scan. Record timeouts, warnings, and baseline pack
checksum repair honestly in evidence.

## Evidence

Evidence is written under
`.aide/queue/Q38-file-quality-ledger-v0/evidence/` and must include changed
files, validation, file quality behavior, docs consistency, test coverage,
reuse/modularity, export-pack sync, and remaining risks.

## Idempotence And Recovery

Re-running Q38 quality generation should overwrite only Q38 quality reports.
If interrupted, resume from `status.yaml`, this plan, the git diff, and
evidence files. Do not infer quality state from chat order.
