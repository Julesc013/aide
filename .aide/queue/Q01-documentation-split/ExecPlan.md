# Q01 ExecPlan: Documentation Split And Canonical Architecture

## Purpose

Q01 will implement an additive documentation split for the AIDE reboot. It prepares durable documentation families around the public model of AIDE Core, AIDE Hosts, and AIDE Bridges while preserving bootstrap-era history, phase records, and evidence.

Q01 is documentation architecture work only. It is not a code refactor, source move, runtime implementation, host implementation, app surface, provider integration, or Q02+ implementation.

## Background And Current Repo Context

AIDE is being rebooted in place. Q00 produced baseline documents under `docs/constitution/`, `docs/charters/`, `docs/reference/`, and `docs/roadmap/`, and Q00 status is currently `needs_review`.

Existing documentation-like surfaces include:

- Root docs: `README.md`, `ROADMAP.md`, `PLANS.md`, `IMPLEMENT.md`, `DOCUMENTATION.md`, `CONTRIBUTING.md`, `MAINTENANCE.md`, and `CHANGELOG.md`.
- Reboot docs: `docs/constitution/bootstrap-era-aide.md`, `docs/charters/reboot-charter.md`, `docs/reference/repo-census.md`, `docs/reference/self-bootstrap.md`, and `docs/roadmap/reboot-roadmap.md`.
- Bootstrap-era doctrine and policy: `governance/**`.
- Bootstrap-era architecture: `specs/**`.
- Source-backed ecosystem research: `research/**`.
- Evaluation reports and blocker summaries: `evals/reports/**`.
- Packaging and release-shape records: `packaging/**`.
- Environment and lab-oriented records: `environments/**` and `labs/**`.
- Agent workflow guidance: `.agents/**`.

Before Q01 implementation begins, the worker must verify Q00 status. If Q00 is still `needs_review`, the worker should proceed only if the prompt or human review explicitly authorizes follow-on Q01 implementation. Otherwise, record the dependency and stop.

## Scope

Q01 implementation should create or update documentation records only. It should define the canonical documentation surface for the reboot and link old documentation areas into the new family structure without moving files.

## Non-goals

- Do not move files.
- Do not delete, hide, or rewrite bootstrap-era records.
- Do not modify implementation code.
- Do not create Runtime, Hosts, Commander, Mobile, IDE extension, provider, CLI, Service, app, packaging, or release implementation.
- Do not implement Q02, Q03, Q04, or later queue items.
- Do not claim future tracks are already implemented.
- Do not broaden support, compatibility, release-readiness, or capability claims beyond existing evidence.

## Allowed Paths For Q01 Implementation

- `docs/**`
- `README.md`
- `DOCUMENTATION.md`
- `ROADMAP.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `.aide/queue/Q01-documentation-split/**`
- `.aide/queue/index.yaml`

## Forbidden Paths For Q01 Implementation

- `shared/**`
- `hosts/**`
- `core/**`
- `bridges/**`
- `evals/**` except references to existing reports if needed
- `packaging/**`
- `governance/**`
- `inventory/**`
- `matrices/**`
- `research/**`
- `environments/**`
- `labs/**`
- implementation code generally

## Planned Documentation Families

Q01 should make the following families navigable:

- `docs/constitution/`: durable doctrine and invariants. Include or link bootstrap-era doctrine and reboot doctrine.
- `docs/charters/`: focused architecture charters for Core, Contract, Harness, Compatibility, Hosts, Bridges, Control, and SDK.
- `docs/roadmap/`: reboot roadmap, queue roadmap, and staged expansion roadmap.
- `docs/design-mining/`: home for extracted lessons from external systems. Q01 should create only a minimal index and candidate list, not full research.
- `docs/decisions/`: ADR-like records for early reboot decisions.
- `docs/reference/`: operational references and user or developer guides.

## Planned Deliverables

Q01 implementation should plan and then create:

- `docs/constitution/README.md`
- `docs/constitution/reboot-doctrine.md` or equivalent additive doctrine record
- `docs/charters/README.md`
- `docs/charters/core-charter.md`
- `docs/charters/contract-charter.md`
- `docs/charters/harness-charter.md`
- `docs/charters/compatibility-charter.md`
- `docs/charters/hosts-charter.md`
- `docs/charters/bridges-charter.md`
- `docs/charters/control-charter.md`
- `docs/charters/sdk-charter.md`
- `docs/roadmap/README.md`
- `docs/roadmap/queue-roadmap.md`
- `docs/roadmap/staged-expansion-roadmap.md`
- `docs/design-mining/README.md`
- `docs/design-mining/candidates.md`
- `docs/decisions/README.md`
- initial decision records for:
  - AIDE reboot in place
  - Core / Hosts / Bridges public model
  - Profile vs Harness distinction
  - Compatibility as first-class
  - XStack remains Dominium-local strict profile
  - Hosts are shells and must not own durable semantics
- `docs/reference/README.md`
- `docs/reference/documentation-migration-map.md`
- `docs/reference/terminology.md` or equivalent terminology normalization reference
- root doc updates to `README.md`, `DOCUMENTATION.md`, `ROADMAP.md`, `PLANS.md`, and `IMPLEMENT.md`
- Q01 evidence under `.aide/queue/Q01-documentation-split/evidence/`

The `docs/design-mining/` candidate list should mention later candidate records for Aider, OpenHands, Cline, Roo Code, Goose, Continue, Cody, GStack, Graphify, Weft, Apfel, Ollama adapters, search adapters, and similar systems without researching them in Q01.

## Milestones

1. Verify Q00 status and read all Q00 outputs.
2. Inspect existing documentation surfaces and record what will be linked, not moved.
3. Draft family indexes for `docs/constitution/`, `docs/charters/`, `docs/roadmap/`, `docs/design-mining/`, `docs/decisions/`, and `docs/reference/`.
4. Draft charter documents for Core, Contract, Harness, Compatibility, Hosts, Bridges, Control, and SDK.
5. Draft decision records for the required early reboot decisions.
6. Draft the documentation migration map.
7. Normalize terminology references.
8. Update root docs only enough to point to the new documentation structure and preserve pre-product honesty.
9. Write Q01 evidence.
10. Run validation and update Q01 status to `needs_review`.

## Progress

- 2026-04-29: Q01 plan-only packet created. No Q01 implementation work was performed.
- 2026-04-29: Q01 implementation started after reading the queue policy, Q00 records, Q01 task packet, root docs, and documentation-like directories. Q00 is still `needs_review`, but the current human prompt explicitly authorized Q01 implementation as the next queue item.
- 2026-04-29: Created Q01 documentation family indexes for constitution, charters, roadmap, design-mining, decisions, and reference.
- 2026-04-29: Added required charters for Core, Contract, Harness, Compatibility, Hosts, Bridges, Control, and SDK.
- 2026-04-29: Added initial ADR-like decision records for reboot-in-place, Core / Hosts / Bridges, Core split, Profile versus Harness, Compatibility, XStack, and host boundaries.
- 2026-04-29: Added documentation migration, terminology, command reference, and generated-artifact reference records.
- 2026-04-29: Updated root docs and Q01 evidence; set Q01 status to `needs_review`.

## Surprises And Discoveries

- 2026-04-29: Q00 is `needs_review`, not `passed`. Q01 implementation should explicitly verify review approval before proceeding.
- 2026-04-29: The current `docs/**` tree is small and reboot-focused; most bootstrap-era documentation remains in existing root, governance, specs, research, evaluation, packaging, environment, and agent directories.
- 2026-04-29: Q01 did not need to edit `governance/**`, `specs/**`, `research/**`, `evals/**`, `packaging/**`, `environments/**`, `.agents/**`, `shared/**`, or `hosts/**`; the migration map could preserve them by reference.

## Decision Log

- 2026-04-29: Q01 planning uses `status: pending` because the existing queue policy does not define a `planning_complete` task state. The status file records `planning_state: planning_complete`.
- 2026-04-29: Q01 should be additive and link/migrate by reference instead of moving or deleting old documentation.
- 2026-04-29: Design-mining records are planned as a documentation home only; Q01 should not perform external-system research.
- 2026-04-29: Root docs are in Q01 implementation scope, but this plan-only task does not rewrite them.
- 2026-04-29: Because Q00 remains review-gated, Q01 will also stop at `needs_review` rather than self-approving. The implementation will preserve Q00 and bootstrap-era records and record this dependency in evidence.
- 2026-04-29: Runtime is documented as part of the internal Core split, but no Runtime charter or implementation is created in Q01 because the prompt required only the listed charters and forbids Runtime work.

## Validation And Acceptance

Q01 implementation is acceptable only when:

- The required documentation families exist and are navigable.
- Required charters exist.
- Required decision records exist.
- Documentation migration map exists.
- Terminology normalization reference or check exists.
- Root docs link the new family structure without becoming marketing pages.
- Bootstrap-era history remains visible.
- Q01 evidence records validation commands and results.
- Q01 changes stay inside allowed paths.
- Q01 status moves to `needs_review`, or `blocked` with a blocker record.

Validation completed on 2026-04-29:

- Required documentation directories exist.
- Required charter files exist.
- Required decision records exist.
- Root docs were updated with Q01 documentation pointers.
- Queue helper scripts ran successfully.
- Terminology scans found the required reboot vocabulary.
- `git diff --check` passed with line-ending normalization warnings only.
- The allowed-path audit passed.
- Detailed command evidence is recorded in `evidence/validation.md`.

This plan-only task is acceptable when:

- `task.yaml`, `ExecPlan.md`, `prompt.md`, `status.yaml`, and `evidence/planning-validation.md` exist under `.aide/queue/Q01-documentation-split/`.
- `.aide/queue/index.yaml` points to the Q01 task packet.
- Queue scripts still run.
- The ExecPlan contains all required sections.
- No implementation docs or forbidden paths are modified.

## Idempotence And Recovery

A stateless worker can restart Q01 by reading:

- `AGENTS.md`
- `.aide/queue/policy.yaml`
- `.aide/queue/index.yaml`
- Q00 status, ExecPlan, and deliverables
- `.aide/queue/Q01-documentation-split/task.yaml`
- `.aide/queue/Q01-documentation-split/ExecPlan.md`
- `.aide/queue/Q01-documentation-split/status.yaml`

If partial Q01 implementation exists, inspect the diff, evidence, and status before editing. Preserve user changes. If forbidden paths were modified, stop and record a blocker. If Q00 remains unreviewed and the prompt does not explicitly authorize proceeding, stop and record the dependency.

## Evidence To Produce

Q01 implementation should produce evidence under `.aide/queue/Q01-documentation-split/evidence/`, including:

- changed-files evidence
- documentation migration evidence
- terminology check evidence
- validation command evidence
- remaining risks and deferrals
- blocker record if blocked

## Outcomes And Retrospective

- Q01 implementation is complete and awaiting review.
- The documentation split is additive and does not move bootstrap-era records.
- The canonical architecture surface now has durable docs for AIDE Core, AIDE Hosts, AIDE Bridges, Contract, Harness, Compatibility, Control, SDK, Dominium Bridge, XStack, bootstrap-era history, and pre-product limits.
- Q01 did not implement Q02 or later work.
