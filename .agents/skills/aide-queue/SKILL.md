---
name: aide-queue
description: Process AIDE filesystem queue items under `.aide/queue/` with bounded paths, status updates, evidence, validation, and review gates.
---

## Use When

- A prompt names an AIDE queue item such as `Q00-bootstrap-audit`.
- Work is non-trivial and should be routed through `.aide/queue/`.
- A future agent needs to claim, run, block, or prepare a queue item for review.

## Workflow

1. Read `AGENTS.md`, `.aide/queue/README.md`, `.aide/queue/policy.yaml`, the task `task.yaml`, `ExecPlan.md`, `prompt.md`, and `status.yaml`.
2. For Profile/Contract-sensitive work, read `.aide/profile.yaml` and `docs/reference/source-of-truth.md`.
3. Confirm the worktree and allowed paths before edits.
4. Update `status.yaml` as work moves through `claimed`, `planning`, `running`, `blocked`, or `needs_review`.
5. Keep edits inside the task allowlist.
6. Write evidence under the task `evidence/` directory.
7. Run proportionate validation and record commands plus results.
8. Stop at blockers and review gates. Do not widen permissions silently.

## Do Not Use For

- Trivial read-only answers covered by bypass policy.
- Product implementation outside an approved queue item.
- Release, publishing, destructive, or secret-access actions without review.
