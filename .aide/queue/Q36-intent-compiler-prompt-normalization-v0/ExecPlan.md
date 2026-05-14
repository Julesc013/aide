# Q36 ExecPlan

## Objective

Implement AIDE's first deterministic intent compiler so raw user requests are
compiled into bounded, safe, repo-grounded WorkUnit drafts before execution.
Q36 produces policy, schemas, AIDE Lite commands, tests, golden tasks, docs,
generated latest intent artifacts, export-pack support, and evidence.

## Scope

Allowed paths are the paths listed in `task.yaml`, with Q36-specific changes
kept to `.aide/policies/intent*.yaml`, `.aide/intake/**`,
`.aide/scripts/aide_lite.py`, `.aide/scripts/tests/**`,
`.aide/evals/golden-tasks/**`, compact docs, generated latest intent artifacts,
and the portable export pack. Generated validation churn outside this scope is
not part of the task diff.

## Non-Goals

- Do not execute the compiled WorkUnit.
- Do not mutate branches, push, merge, prune, tag, publish, or call GitHub APIs.
- Do not mutate Eureka, Dominium, or external repositories.
- Do not call providers, models, outbound network services, embeddings, or
  vector search.
- Do not implement Q37 Repo Intelligence Index v0 or later refactor/install
  phases.

## Milestones

1. Confirm Q35 passed and Q36 can proceed from repo-local state.
2. Update the Q36 queue packet and intent governance policy.
3. Define WorkUnit sizing, task/risk class, and prompt-normalization policies.
4. Add intent packet and WorkUnit draft schemas plus examples.
5. Implement `aide_lite.py intent compile|validate|examples|status`.
6. Add unittest and golden task coverage for safe prompt normalization.
7. Update docs and generated latest Q37 intent/workunit artifacts.
8. Regenerate the portable pack and record evidence.
9. Run validation and move Q36 to `needs_review`.

## Progress

- 2026-05-14: Q35 status inspected and found passed. Baseline Harness and AIDE
  Lite checks passed; broad generated validation outputs were restored before
  Q36 edits to keep scope bounded.
- 2026-05-14: Q36 packet moved from planned to implementation state and this
  ExecPlan expanded for restartable execution.

## Decisions

- Direct edits and commits occur on `main` because the prompt requires commits
  and also forbids branch mutation. The branch policy warning is recorded as a
  risk rather than repaired by creating a task branch.
- Q36 confidence is heuristic and deterministic. It must not overclaim semantic
  understanding or use a model.
- Long prompt storage is prohibited. The compiler stores a SHA-256 hash and a
  bounded excerpt only.

## Validation Intent

Run proportionate checks: `git diff --check`, AIDE Lite intent commands,
targeted Q36 unittest discovery, full AIDE Lite tests when practical, golden
tasks, Harness/Core unittest suites, export-pack and pack-status, and secret
scan. Record any timeout, warning, or restored generated-output churn honestly
in evidence.

## Evidence

Evidence is written under
`.aide/queue/Q36-intent-compiler-prompt-normalization-v0/evidence/` and must
include changed files, validation, intent compiler behavior, prompt
normalization behavior, WorkUnit sizing, export-pack sync, and remaining risks.

## Idempotence And Recovery

Re-running Q36 command generation should overwrite only Q36 latest intent and
WorkUnit draft outputs. If interrupted, resume from `status.yaml`, this plan,
the git diff, and evidence files. Do not replay raw chat history as truth.
