# Q39 ExecPlan

## Objective

Implement AIDE's first deterministic Refactor Control Plane so structural
change can be planned, dry-run, validated, reviewed, and recorded before any
future apply phase moves, deletes, rewrites, migrates, or refactors files.

## Scope

Allowed paths are the paths listed in `task.yaml`. Q39-specific changes stay
inside refactor policies, `.aide/refactors/**`, AIDE Lite refactor commands,
Q39 tests and golden tasks, compact documentation, generated Q40 context
artifacts, export-pack support, and this queue packet.

## Non-Goals

- Do not move, delete, rename, rewrite references, refactor, migrate, absorb,
  install, upgrade, repair, roll back, or release anything.
- Do not create concrete current move/salvage maps for an actual root.
- Do not call providers, models, outbound network services, embeddings, or
  vector search.
- Do not mutate branches, push, merge, prune, tag, publish, call GitHub APIs,
  or install active workflows.
- Do not mutate Eureka, Dominium, or external repositories.
- Do not implement Q40 Root Recycling Framework v0 or later phases.

## Milestones

1. Confirm Q38 file quality outputs exist and record baseline validation.
2. Create the Q39 queue packet and add it to the filesystem queue index.
3. Define refactor, migration, safety, evidence, and application policies.
4. Add refactor plan, operation, move-map, salvage-map, path-alias,
   migration-ledger, rollback, risk, and validation schemas.
5. Implement `aide_lite.py refactor status|plan|validate|dry-run|schemas|ledger`.
6. Add deterministic unittest coverage and golden tasks.
7. Generate readiness, no-apply example plan, and migration-ledger example
   artifacts.
8. Update docs, command catalog, and Q40 latest task packet references.
9. Regenerate the portable export pack and record evidence.
10. Run validation and move Q39 to `needs_review`.

## Progress

- 2026-05-14: Q38 status inspected and found implemented with `needs_review`;
  file quality ledger and reports are present. Baseline validation passed with
  known generated-manifest warnings and conservative repo/quality warnings.
- 2026-05-14: Q39 queue packet created with this restartable ExecPlan.

## Decisions

- Direct edits and commits occur on `main` because the prompt requires commits
  and forbids branch mutation. Branch-policy risk is recorded rather than fixed
  by creating a task branch.
- Q39 plans are no-apply artifacts. Any future apply phase must be separately
  authorized and review-gated.
- `drop_candidate` is not deletion approval. `archive`, `shim`, and `alias`
  are planned fates only.
- Target repositories must generate their own refactor readiness and plans
  after import; AIDE source-generated latest plans are not target truth.

## Validation Intent

Run proportionate checks: `git diff --check`, refactor commands, targeted Q39
unittest discovery, AIDE Lite tests, golden tasks, Harness/Core unittest suites,
export-pack and pack-status, repo/quality/intent validation, command catalog
validation, and a targeted secret scan. Record warnings, timeouts, and dry-run
no-op guarantees honestly in evidence.

## Evidence

Evidence is written under
`.aide/queue/Q39-refactor-control-plane-v0/evidence/` and must include changed
files, validation, refactor control behavior, schema behavior, dry-run proof,
migration-ledger readiness, export-pack sync, and remaining risks.

## Idempotence And Recovery

Re-running Q39 refactor planning should overwrite only Q39 readiness/example
artifacts under `.aide/refactors/**`. If interrupted, resume from
`status.yaml`, this plan, the git diff, and evidence files. Do not infer
refactor state from chat order.
