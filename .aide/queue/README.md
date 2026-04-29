# AIDE Filesystem Queue

`.aide/queue/` is the canonical task queue for AIDE self-hosting work. The Codex extension UI, chat history, and ad hoc prompts can help operate the queue, but they are not the source of truth.

## Queue Model

- `index.yaml` records queue order and planned task packets.
- `policy.yaml` records execution policy, task states, evidence requirements, and stop conditions.
- Each non-trivial queue item gets its own directory with at least `task.yaml`, `ExecPlan.md`, `prompt.md`, `status.yaml`, and `evidence/`.
- ExecPlans are the durable unit of long-running autonomous work.

## Task States

- `pending`: queued but not claimed.
- `claimed`: a worker has taken responsibility.
- `planning`: scope and validation are being refined before edits.
- `running`: bounded work is in progress.
- `blocked`: work cannot continue without explicit blocker resolution.
- `needs_review`: implementation stopped at a review gate or completion review.
- `passed`: review accepted the task.
- `failed`: review rejected the task or validation failed in a way that ends the attempt.
- `superseded`: replaced by a later queue item or decision.

## Evidence And Review Gates

Every substantial queue item must produce evidence in its `evidence/` directory. Evidence should name the files changed, validation commands run, outcomes, unresolved blockers, and deliberate deferrals.

Workers must stop at hard review gates. Review gates include permission widening, destructive commands, secret access, source-of-truth changes for generated artifacts, compatibility or migration changes, release or publishing actions, merge-to-main actions, and changes to the queue or autonomy policies themselves.

## Processing Rules For Future Agents

1. Read `AGENTS.md`, this README, `policy.yaml`, the task `task.yaml`, `ExecPlan.md`, `prompt.md`, and `status.yaml`.
2. Confirm allowed paths before edits.
3. Update `status.yaml` as the task moves through states.
4. Keep the ExecPlan current as a living document.
5. Make the smallest coherent change set.
6. Run proportionate validation.
7. Write evidence before asking for review.
8. Stop at blockers or review gates instead of widening scope silently.

