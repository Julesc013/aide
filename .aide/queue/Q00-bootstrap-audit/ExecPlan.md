# Q00 ExecPlan: Baseline Freeze And Reboot Audit

## Purpose

Q00 freezes the factual baseline for the AIDE in-place reboot. A future worker must verify what already exists, record the self-hosting queue posture, and produce evidence that Q01 can proceed without erasing bootstrap-era history.

Q00 is not the implementation of Q01, Q02, Q03, Q04, or any later queue item.

## Current Repo Facts To Verify

- `AGENTS.md` defines repository operating law and requires plan-first behavior for complex work.
- `README.md`, `ROADMAP.md`, `PLANS.md`, `IMPLEMENT.md`, and `DOCUMENTATION.md` describe the completed bootstrap and implementation phase history.
- The repository has existing `shared/`, `hosts/`, `evals/`, `packaging/`, `governance/`, `inventory/`, `matrices/`, `research/`, `environments/`, and `labs/` trees that must be preserved.
- `.aide/queue/` exists as the canonical filesystem queue after the self-bootstrap scaffold.
- The current reboot focus is Contract, Harness, Compatibility, and Dominium Bridge, with XStack as Dominium's strict local governance and proof profile.
- Any fact above must be rechecked from files before it is treated as evidence.

## Scope

Q00 may read the repository broadly to establish baseline facts. Q00 may only edit the allowed paths named in `task.yaml`, and should prefer writing status and evidence under `.aide/queue/Q00-bootstrap-audit/`.

## Non-goals

- Do not implement Q01 or later queue items.
- Do not create product runtime, broker, service, host, IDE extension, Commander, Mobile, or app-surface code.
- Do not change `shared/**`, `hosts/**`, `evals/**`, `packaging/**`, `governance/**`, `inventory/**`, `matrices/**`, `research/**`, `environments/**`, `labs/**`, `specs/**`, or `fixtures/**`.
- Do not fabricate support, capability, compatibility, release-readiness, or parity claims.
- Do not create tags, push branches, publish artifacts, or merge to main.

## Allowed Paths

- `AGENTS.md`
- `README.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`
- `docs/**`
- `.aide/**`
- `.agents/**`
- `scripts/**`

## Milestones

1. Claim Q00 by updating `status.yaml` from `pending` to `claimed`.
2. Re-read all governing files named by the prompt and this ExecPlan.
3. Inspect the repository structure and record the baseline without changing forbidden paths.
4. Validate the queue scaffold and scripts.
5. Write evidence with commands, results, blockers, and deferrals.
6. Update this ExecPlan with progress, discoveries, decisions, validation, and retrospective notes.
7. Move `status.yaml` to `needs_review` if accepted criteria are met, or `blocked` if a hard blocker remains.

## Progress

- 2026-04-29: Self-bootstrap scaffold created this ExecPlan and marked Q00 ready for a future worker.
- Q00 audit work has not been performed yet.

## Surprises And Discoveries

- None yet. Future workers should append dated entries instead of replacing this section.

## Decision Log

- 2026-04-29: Q00 is a baseline audit and review gate, not the first implementation step for later queue work.
- 2026-04-29: Queue evidence lives with the task so a stateless future worker can recover context from the filesystem.

## Validation And Acceptance

Q00 is acceptable only when:

- Required Q00 task files exist.
- Queue policy and status are internally consistent.
- `scripts/aide-queue-status` and `scripts/aide-queue-next` run through Python with no external dependencies.
- Changed paths are audited against the allowed and forbidden lists.
- Evidence records the commands and results.
- `status.yaml` reflects `needs_review` or `blocked` honestly.

## Idempotence And Recovery

A stateless worker can restart Q00 by reading `AGENTS.md`, `.aide/queue/README.md`, `.aide/queue/policy.yaml`, this `ExecPlan.md`, `task.yaml`, `prompt.md`, and `status.yaml`.

If prior work exists, inspect the current diff and evidence before editing. Preserve unrelated user changes. Re-run validation after any change. If the worktree is too dirty to distinguish Q00 changes from unrelated changes, record the blocker in evidence and stop.

## Evidence To Produce

- A baseline audit note under `.aide/queue/Q00-bootstrap-audit/evidence/`.
- A validation summary naming commands and outcomes.
- A changed-file list.
- A blocker and deferral list.
- Any review-gate trigger that stopped work.

## Outcomes And Retrospective

- Pending. Future workers should complete this section before moving Q00 to `needs_review` or `blocked`.

