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

<!-- AIDE-GENERATED:BEGIN section=aide-execplan-source-summary generator=aide-harness-generated-artifacts-v0 version=q05.generated-artifacts.v0 mode=managed-section sources=.aide/profile.yaml,.aide/toolchain.lock,.aide/commands/catalog.yaml,.aide/queue/policy.yaml,.aide/queue/index.yaml,docs/reference/source-of-truth.md,docs/reference/harness-v0.md,docs/reference/generated-artifacts-v0.md fingerprint=sha256:554d90b21fb6ab0e845bcd2e0db2badcfaebd35da346afaa69502e67d7ac2182 manual=outside-only -->
## Generated AIDE Source Summary

- ExecPlans are the restartable control document for long-running AIDE queue work.
- Keep Progress, discoveries, decisions, validation, recovery, evidence, and retrospective current while work runs.
- Do not use an ExecPlan to widen scope beyond the queue task allowlist.
- Generated outputs must be treated as reviewable downstream artifacts, not canonical plans.
<!-- AIDE-GENERATED:END section=aide-execplan-source-summary -->
