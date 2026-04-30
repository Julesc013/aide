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

<!-- AIDE-GENERATED:BEGIN section=aide-queue-source-summary generator=aide-harness-generated-artifacts-v0 version=q05.generated-artifacts.v0 mode=managed-section sources=.aide/profile.yaml,.aide/toolchain.lock,.aide/commands/catalog.yaml,.aide/queue/policy.yaml,.aide/queue/index.yaml,docs/reference/source-of-truth.md,docs/reference/harness-v0.md,docs/reference/generated-artifacts-v0.md fingerprint=sha256:979066316b75a7655319dd8373c39c6b18452c411495e49ef2dae8f0cacc7bae manual=outside-only -->
## Generated AIDE Source Summary

- Read `.aide/profile.yaml`, `.aide/queue/policy.yaml`, and the active queue packet before editing.
- `.aide/queue/` is canonical for long-running task state; extension task queues are not canonical.
- Generated downstream artifacts are not source of truth and must preserve provenance markers.
- Stop at review gates, write evidence, and keep changes inside the task allowlist.
<!-- AIDE-GENERATED:END section=aide-queue-source-summary -->
