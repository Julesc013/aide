# Q37 ExecPlan

## Objective

Implement AIDE's first deterministic Repo Intelligence Index so the repository
can be inspected through structured, local, reproducible maps before future
quality, refactor, root recycling, install, or upgrade work acts on files.

## Scope

Allowed paths are the paths listed in `task.yaml`, with Q37-specific changes
kept to repo-intelligence policies, `.aide/repo/**`, `.aide/scripts/aide_lite.py`,
`.aide/scripts/tests/**`, golden tasks, compact docs, generated Q38 context
artifacts, export-pack support, and this queue packet. Generated validation
churn outside this scope is not part of the task diff.

## Non-Goals

- Do not move, delete, rename, refactor, migrate, absorb, or rewrite files.
- Do not declare files dead; Q37 only emits conservative candidates.
- Do not call providers, models, outbound network services, embeddings, or
  vector search.
- Do not mutate branches, push, merge, prune, tag, publish, call GitHub APIs,
  or install active workflows.
- Do not mutate Eureka, Dominium, or external repositories.
- Do not implement Q38 File Quality Ledger v0 or later refactor/install phases.

## Milestones

1. Confirm Q36 intent compiler outputs exist and current repo state is clean.
2. Create the Q37 queue packet and record baseline validation.
3. Define repo intelligence, classification, ownership, dependency, test, and
   doc-link policies plus schemas.
4. Implement `aide_lite.py repo inventory|classify|validate|status|explain-file|docs|tests|deps`.
5. Add deterministic unittest coverage and golden tasks.
6. Generate repo intelligence indexes and compact Markdown summary.
7. Update docs, command catalog, and Q38 latest task packet references.
8. Regenerate the portable export pack and record evidence.
9. Run validation and move Q37 to `needs_review`.

## Progress

- 2026-05-14: Q36 status inspected and found implemented with `needs_review`.
  Baseline Git, Harness, AIDE Lite, intent, export, and test commands were run.
  Baseline generated preview/report churn outside Q37 scope was restored before
  Q37 edits.
- 2026-05-14: Q37 queue packet created with this restartable ExecPlan.
- 2026-05-14: Q37 policies, schemas, commands, tests, golden tasks, docs,
  generated repo intelligence outputs, Q38 context packet, export-pack sync,
  and evidence were completed. The task is stopped at `needs_review`.

## Decisions

- Direct edits and commits occur on `main` because the prompt requires commits
  and forbids branch mutation. Branch-policy risk is recorded rather than fixed
  by creating a task branch.
- Q37 classification is path, extension, and pattern based. It must not
  overclaim semantic understanding.
- Orphan outputs use candidate language only and never recommend deletion.
- Target repositories must generate their own repo intelligence outputs after
  import; AIDE source-generated indexes are not target truth.

## Validation Intent

Run proportionate checks: `git diff --check`, repo intelligence commands,
targeted Q37 unittest discovery, AIDE Lite tests, golden tasks, Harness/Core
unittest suites, export-pack and pack-status, intent validation, command catalog
validation, and a targeted secret scan. Record timeouts, warnings, and restored
generated-output churn honestly in evidence.

## Evidence

Evidence is written under
`.aide/queue/Q37-repo-intelligence-index-v0/evidence/` and must include changed
files, validation, repo intelligence behavior, file classification, ownership,
dependency/test/doc maps, export-pack sync, and remaining risks.

## Idempotence And Recovery

Re-running Q37 index generation should overwrite only Q37 repo intelligence
outputs. If interrupted, resume from `status.yaml`, this plan, the git diff,
and evidence files. Do not infer repo facts from chat order.
