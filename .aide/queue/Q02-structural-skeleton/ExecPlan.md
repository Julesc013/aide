# Q02 ExecPlan: Minimal Self-Hosting Structural Skeleton

## Purpose

Q02 will introduce the target AIDE structural skeleton additively and safely. The future implementation should create only skeleton directories, README files, migration maps, and conceptual ownership boundaries for AIDE Core, AIDE Hosts, and AIDE Bridges.

Q02 is not a deep code migration. It must preserve bootstrap-era source layout, tests, imports, host proof records, phase history, and evidence. Q02 does not implement Q03, Q04, Runtime, Service, Commander, Mobile, IDE extensions, provider adapters, app surfaces, or automated service logic.

## Background And Current Repo Context

AIDE is being rebooted in place. Q00 and Q01 are both present and both currently have `status: needs_review`.

Current facts verified during Q02 planning:

- Q00 produced the bootstrap-era baseline, reboot charter, repo census, and reboot roadmap.
- Q01 produced architecture charters, decision records, terminology references, and documentation family indexes.
- The current repository has top-level `shared/`, `hosts/`, `governance/`, `inventory/`, `matrices/`, `research/`, `specs/`, `environments/`, `labs/`, `evals/`, `packaging/`, `scripts/`, `.agents/`, `.aide/`, and `docs/` trees.
- The current repository does not yet have top-level `core/` or `bridges/` directories.
- The current `hosts/` directory already contains bootstrap-era proof lanes under `hosts/apple/**`, `hosts/microsoft/**`, `hosts/metrowerks/**`, and `hosts/templates/**`.
- The current `shared/**` tree contains executable bootstrap-era Python shared-core code, tests, schemas, and CLI bridge material that must remain in place by default.

Because Q00 and Q01 are still review-gated, a future Q02 implementation worker should proceed only if the human prompt explicitly authorizes implementation or the prior queue items have been reviewed and accepted.

## Scope

Q02 implementation should create an additive skeleton for the target conceptual structure and explain how current bootstrap-era directories map into it. It may add README files and mapping documents. It may update root documentation only enough to point to the new skeleton and migration map.

## Non-goals

- Do not implement Q03, Q04, Q05, Q06, Q07, Q08, or later queue items.
- Do not move, delete, or rewrite bootstrap-era records.
- Do not refactor implementation code.
- Do not change current imports, package names, tests, runtime behavior, host proofs, adapters, or fixtures.
- Do not create a real Runtime, broker, scheduler, router, service, worker, transport, state/cache system, Commander, Mobile surface, IDE extension implementation, provider adapter, app surface, package, release, or autonomous runner.
- Do not promote candidate host families into committed implementation.
- Do not claim the first shipped stack is implemented by Q02.

## Allowed Paths For Q02 Implementation

- `core/**`
- `hosts/README.md`
- `hosts/cli/**`
- `hosts/service/**`
- `hosts/commander/**`
- `hosts/extensions/**`
- `bridges/**`
- `docs/**`
- `README.md`
- `DOCUMENTATION.md`
- `ROADMAP.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `.aide/queue/Q02-structural-skeleton/**`
- `.aide/queue/index.yaml`

## Forbidden Paths For Q02 Implementation

- `shared/**` except read-only inspection and documentation references.
- Existing `hosts/apple/**`, `hosts/microsoft/**`, `hosts/metrowerks/**`, and `hosts/templates/**` implementation or proof files except additive README or mapping notes only if necessary and safe.
- `governance/**`
- `inventory/**`
- `matrices/**`
- `research/**`
- `environments/**`
- `labs/**`
- `evals/**`
- `packaging/**`
- `scripts/**`
- implementation code generally
- any move/delete of bootstrap-era files

## Target Skeleton

Q02 implementation should plan for this public target structure:

- `core/`
- `hosts/`
- `bridges/`
- `docs/`
- `labs/`
- `scripts/`

The `docs/`, `labs/`, `scripts/`, and `hosts/` directories already exist. Q02 should not move them. It should add only the new skeleton surfaces that are missing or safe to add.

Target internal Core structure:

- `core/contract/`
- `core/harness/`
- `core/runtime/`
- `core/compat/`
- `core/control/`
- `core/sdk/`
- `core/tests/`

Target Hosts structure:

- `hosts/cli/`
- `hosts/service/`
- `hosts/commander/`
- `hosts/extensions/`
- `hosts/extensions/visualstudio/`
- `hosts/extensions/vscode/`
- `hosts/extensions/xcode/`
- `hosts/extensions/later/`

Target Bridges structure:

- `bridges/dominium/`
- `bridges/dominium/xstack/`
- `bridges/dominium/profiles/`
- `bridges/dominium/policies/`
- `bridges/dominium/generators/`

## Current-To-Target Mapping Strategy

Default strategy: preserve current physical locations and add conceptual mappings. Do not move code.

Planned mapping:

- `shared/` remains in place. It maps conceptually to future `core/contract/`, `core/harness/`, `core/runtime/`, and `core/tests/` depending on subarea. Q02 should not migrate it.
- Existing `hosts/apple/**`, `hosts/microsoft/**`, `hosts/metrowerks/**`, and `hosts/templates/**` remain in place as bootstrap-era proof lanes and templates. They map conceptually to future `hosts/extensions/*` or retained proof history.
- `governance/**`, `inventory/**`, `matrices/**`, `research/**`, `environments/**`, `evals/**`, and `packaging/**` remain in place. They map conceptually to future `core/control/` and `core/compat/` inputs but are not moved.
- `scripts/**` remains in place. It maps conceptually to future Harness and CLI support, but Q02 should not move scripts.
- `.agents/**` remains in place. It maps to portable skills and maintained agent guidance.
- `.aide/**` remains in place. It remains the canonical self-hosting contract, queue, policy, status, and evidence surface.
- `bridges/dominium/**` is new skeleton space only. It must not implement the bridge until Q07.

The structural migration map should include columns for current physical location, conceptual home, move status, and notes. Move status values should include `keep`, `shim`, `future_move`, `candidate`, and `deferred`.

## Planned Deliverables

Q02 implementation should create or update these files:

- `core/README.md`
- `core/contract/README.md`
- `core/harness/README.md`
- `core/runtime/README.md`
- `core/compat/README.md`
- `core/control/README.md`
- `core/sdk/README.md`
- `core/tests/README.md`
- `hosts/README.md`
- `hosts/cli/README.md`
- `hosts/service/README.md`
- `hosts/commander/README.md`
- `hosts/extensions/README.md`
- `hosts/extensions/visualstudio/README.md`
- `hosts/extensions/vscode/README.md`
- `hosts/extensions/xcode/README.md`
- `hosts/extensions/later/README.md`
- `bridges/README.md`
- `bridges/dominium/README.md`
- `bridges/dominium/xstack/README.md`
- `bridges/dominium/profiles/README.md`
- `bridges/dominium/policies/README.md`
- `bridges/dominium/generators/README.md`
- `docs/reference/structural-migration-map.md`
- root doc updates to `README.md`, `DOCUMENTATION.md`, `ROADMAP.md`, `PLANS.md`, and `IMPLEMENT.md`
- Q02 evidence:
  - `.aide/queue/Q02-structural-skeleton/evidence/changed-files.md`
  - `.aide/queue/Q02-structural-skeleton/evidence/validation.md`
  - `.aide/queue/Q02-structural-skeleton/evidence/structural-map.md`
  - `.aide/queue/Q02-structural-skeleton/evidence/remaining-risks.md`

README content expectations:

- Core README: define AIDE Core as host-agnostic durable substance and explain Contract, Harness, Runtime, Compatibility, Control, and SDK as skeleton bands.
- Contract README: define profiles, schemas, commands, policies, tasks, eval declarations, component maps, and environment declarations; state contract v0 is Q03.
- Harness README: define import, compile, validate, doctor, bakeoff, migrate, and drift check machinery; state Harness v0 is Q04.
- Runtime README: define broker, scheduler, router, context service, patch engine, approvals, workers, transport, and state/cache; state runtime is deferred.
- Compatibility README: define schema versions, migrations, replay corpora, shims, upgrade gates, and deprecation rules; state baseline is Q06.
- Control README: define eval inventories, environment records, matrices, packaging metadata, benchmarks, and cost/latency envelopes; map existing control-plane areas without moving them.
- SDK README: define future host client APIs, service APIs, protocol bindings, generated artifact consumers, host capability descriptors, and patch/approval/replay schemas; state SDK is planned.
- Core tests README: define future cross-Core tests and state existing tests remain where they are.
- Hosts README: define hosts as shells and list CLI, Service, Commander, Mobile later, and IDE/editor extensions later.
- CLI README: define CLI as first low-friction host for Harness and future Runtime commands; state existing scripts and CLI bridge remain in old locations until migrated safely.
- Service README: define future broker/service host; state Q02 does not implement it.
- Commander README: define future desktop command deck; state Q02 does not implement it.
- Extensions README and family placeholders: define thin OEM/editor shells and avoid implying committed implementation beyond current evidence.
- Bridges README: define Bridges as downstream/project-specific overlays and state provider/tool/protocol adapters are not Bridges.
- Dominium README and subfolders: define Dominium Bridge skeleton and keep XStack Dominium-local; state Q07 owns baseline bridge implementation.

## Milestones

1. Verify Q00 and Q01 status, outputs, and review posture.
2. Read root docs and inspect the current top-level tree.
3. Confirm current `shared/**`, `hosts/**`, control-plane, docs, scripts, `.agents/**`, and `.aide/**` locations.
4. Create additive skeleton directories and README files only in allowed paths.
5. Add `docs/reference/structural-migration-map.md`.
6. Update root docs minimally and record Q02 in `IMPLEMENT.md`.
7. Write Q02 evidence.
8. Run structural validation, queue helper checks, terminology scans, allowed-path audit, and import-preservation checks.
9. Set Q02 status to `needs_review` if complete, or `blocked` with evidence if not.

## Progress

- 2026-04-29: Q02 plan-only packet created. No Q02 implementation work was performed.

## Surprises And Discoveries

- 2026-04-29: Q00 and Q01 both remain `needs_review`; Q02 implementation should require explicit authorization or accepted prior reviews before editing the structural skeleton.
- 2026-04-29: Top-level `hosts/` already exists and contains bootstrap-era proof lanes, so Q02 must treat new host categories as additive subtrees without disturbing existing lanes.
- 2026-04-29: Top-level `core/` and `bridges/` are absent, making them safe planned additions for a future implementation task.

## Decision Log

- 2026-04-29: Q02 planning uses `status: pending` because `planning_complete` is not a queue-policy task state; `planning_state: planning_complete` records that planning is complete.
- 2026-04-29: The default Q02 implementation strategy is no code moves. Any tiny safe move with compatibility shim is discouraged and would need explicit review-gate handling.
- 2026-04-29: Existing `hosts/**` proof lanes remain bootstrap-era evidence, not targets for relocation in Q02.
- 2026-04-29: `bridges/dominium/**` is planned as skeleton only; Dominium Bridge baseline implementation remains Q07.

## Validation And Acceptance

This plan-only task is acceptable when:

- `.aide/queue/Q02-structural-skeleton/task.yaml` exists.
- `.aide/queue/Q02-structural-skeleton/ExecPlan.md` exists and contains all required sections.
- `.aide/queue/Q02-structural-skeleton/prompt.md` exists.
- `.aide/queue/Q02-structural-skeleton/status.yaml` exists.
- `.aide/queue/Q02-structural-skeleton/evidence/planning-validation.md` exists.
- `.aide/queue/index.yaml` references the Q02 task, ExecPlan, prompt, and evidence path.
- `PLANS.md` contains only a minimal Q02 planning pointer.
- No `core/**`, `bridges/**`, or new host skeleton directories were created by the plan-only task.
- No forbidden paths were modified.

Q02 implementation will be acceptable only when:

- Required skeleton README files exist and remain clearly labeled as skeleton/planned/deferred where appropriate.
- `docs/reference/structural-migration-map.md` exists and maps current physical locations to conceptual homes and move statuses.
- Current tests and imports are preserved.
- Bootstrap-era host proof history remains visible.
- Root docs link the skeleton without overstating implementation.
- Q02 evidence records commands and results.
- Q02 status moves to `needs_review` or `blocked` honestly.

## Idempotence And Recovery

A stateless worker can restart Q02 by reading:

- `AGENTS.md`
- `.aide/queue/policy.yaml`
- `.aide/queue/index.yaml`
- Q00 status, ExecPlan, and outputs
- Q01 status, ExecPlan, charters, and migration map
- `.aide/queue/Q02-structural-skeleton/task.yaml`
- `.aide/queue/Q02-structural-skeleton/ExecPlan.md`
- `.aide/queue/Q02-structural-skeleton/status.yaml`

If partial Q02 implementation already exists, inspect `git status`, `git diff`, Q02 evidence, and queue status before editing. Preserve unrelated user changes. If `core/**`, `bridges/**`, or new host skeleton files were created before the implementation task, determine whether they are Q02-owned; if not, stop and record a blocker. If forbidden paths were modified, stop and record a blocker. Re-run validation after any correction.

## Evidence To Produce

Q02 implementation should produce:

- `.aide/queue/Q02-structural-skeleton/evidence/changed-files.md`
- `.aide/queue/Q02-structural-skeleton/evidence/validation.md`
- `.aide/queue/Q02-structural-skeleton/evidence/structural-map.md`
- `.aide/queue/Q02-structural-skeleton/evidence/remaining-risks.md`
- `.aide/queue/Q02-structural-skeleton/evidence/blocker.md` if blocked

## Outcomes And Retrospective

- Pending future Q02 implementation.
- This plan-only packet does not create the structural skeleton.
