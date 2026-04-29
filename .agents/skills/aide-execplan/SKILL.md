---
name: aide-execplan
description: Create and maintain restartable AIDE ExecPlans as living documents for long-running queue work.
---

## Use When

- A queue item needs an `ExecPlan.md`.
- A stateless future worker must be able to resume work from the filesystem.
- Work spans multiple steps, files, blockers, or validation phases.

## ExecPlan Requirements

- State the purpose, scope, non-goals, allowed paths, milestones, validation, and evidence.
- Include current facts to verify rather than unverified assumptions.
- Maintain progress, surprises, decisions, and retrospective notes as the work changes.
- Describe idempotence and recovery so a new worker can continue safely.
- Keep the plan self-contained enough that chat history is optional.

## Operating Rule

Treat the ExecPlan as a living control document. Update it during execution, not only after completion. Never use it to smuggle in scope beyond the task allowlist.

