# Q03 ExecPlan: Profile Contract v0

## Purpose

Q03 will define the first minimal AIDE Profile/Contract v0 and instantiate it for the AIDE self-hosting repository. The Profile is a declarative repo contract: it says what this repository declares, requires, allows, owns, exposes, and defers. It is not executable machinery.

Q03 is the Contract/Profile step after Q00 baseline audit, Q01 documentation split, and Q02 structural skeleton. It must not implement Q04 Harness v0, generated artifacts, Runtime, Hosts, Commander, Mobile, IDE extension families, provider adapters, app surfaces, or autonomous service logic.

## Background And Current Repo Context

AIDE is being rebooted in place. Bootstrap-era documents, phase records, source files, host proof lanes, eval records, packaging records, environment records, and evidence must remain visible and unmoved.

Current facts to verify before Q03 implementation:

- Q00, Q01, and Q02 exist and currently stop at `needs_review`.
- Q00 produced the bootstrap-era baseline, reboot charter, repo census, and reboot roadmap.
- Q01 produced documentation families, architecture charters, ADR-like decisions, terminology records, and documentation migration mapping.
- Q02 produced README-only skeletons for `core/`, future host categories, `bridges/`, Dominium Bridge, and `docs/reference/structural-migration-map.md`.
- `.aide/profile.yaml` and `.aide/toolchain.lock` already exist as minimal P15 bootstrap scaffold records. Q03 should refine or replace their content carefully into Contract v0 rather than treating them as absent.
- `.aide/queue/` remains canonical for queue execution state. It is not a substitute for product doctrine or the Profile contract.
- Existing `.aide/policies/autonomy.yaml`, `.aide/policies/bypass.yaml`, and `.aide/policies/review-gates.yaml` exist and must not be loosened.
- `core/contract/README.md` is currently skeleton-only and says actual profile and contract v0 is Q03.

If Q00, Q01, or Q02 remains `needs_review`, a future Q03 implementation worker should proceed only if the human prompt explicitly authorizes Q03 implementation after review consideration. Otherwise, record the dependency and stop.

## Scope

Q03 implementation should create a small, enforceable, reviewable Contract/Profile v0 for this repository. It should define the `.aide/` contract layout, status-labeled declarations, minimal schema or documented-shape strategy, source-of-truth rules, and human references.

Q03 may update root docs and agent guidance only enough to explain the new profile contract and how agents should find it. Q03 evidence should live under `.aide/queue/Q03-profile-contract-v0/evidence/`.

## Non-goals

- Do not implement Q04 Harness commands.
- Do not implement generated artifacts or downstream files such as `CLAUDE.md` or `.claude/**`; generated artifacts remain Q05.
- Do not build Runtime, Service, Commander, Mobile, IDE extension implementation, provider adapters, app surfaces, package automation, release automation, or autonomous worker invocation.
- Do not move or refactor source code.
- Do not migrate the bootstrap-era `shared/**` implementation.
- Do not edit existing host proof files.
- Do not loosen autonomy, bypass, review-gate, compatibility, ownership, generated-artifact, or validation severity policy.
- Do not make `.aide/` a shadow product architecture. It is the declarative self-hosting contract and queue surface.
- Do not claim future Runtime, Hosts, Bridges, generated artifacts, or Harness features are already implemented.

## Allowed Paths For Q03 Implementation

- `.aide/profile.yaml`
- `.aide/toolchain.lock`
- `.aide/components/**`
- `.aide/commands/**`
- `.aide/policies/**`
- `.aide/tasks/**`
- `.aide/evals/**`
- `.aide/adapters/**`
- `.aide/compat/**`
- `core/contract/**`
- `docs/reference/profile-contract-v0.md`
- `docs/reference/source-of-truth.md`
- `AGENTS.md`
- `.agents/skills/**`
- `README.md`
- `DOCUMENTATION.md`
- `ROADMAP.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `.aide/queue/Q03-profile-contract-v0/**`
- `.aide/queue/index.yaml`

## Forbidden Paths For Q03 Implementation

- `shared/**`
- existing `hosts/**` implementation/proof files
- `bridges/**` except references to future Dominium Bridge if needed
- `core/harness/**`
- `core/runtime/**`
- `core/compat/**` except conceptual references from Contract docs if needed
- `core/control/**` except conceptual references from Contract docs if needed
- `core/sdk/**`
- `governance/**`
- `inventory/**`
- `matrices/**`
- `research/**`
- `environments/**`
- `labs/**`
- `evals/**`
- `packaging/**`
- implementation code generally
- generated downstream artifacts such as `CLAUDE.md` or `.claude/**`

## Contract/Profile Model

Q03 must keep these concepts separate:

- Profile: declarative repository contract. It states repository identity, lifecycle status, public model, implemented reality, future intent, owned paths, declared commands, policies, task classes, eval declarations, adapter metadata, compatibility posture, and source-of-truth rules.
- Harness: executable machinery planned for Q04. It will later import, compile, validate, doctor, bakeoff, migrate, and drift-check the Profile. Q03 may define command declarations, but it must not implement the command behavior.

The Q03 Profile/Contract v0 should be small enough that a future standard-library Harness can validate it. Use explicit status values such as `implemented`, `partial`, `planned`, `deferred`, and `candidate` so the contract does not overstate the current pre-product repository.

## Planned `.aide/` Layout

Q03 implementation should instantiate the contract with a compact layout:

- `.aide/profile.yaml`: canonical self-hosting profile for this repository. It should include repo id/name, repo role, lifecycle `reboot/pre-product`, profile mode `self-hosting`, current public model, first shipped stack, profile schema version, implemented reality, and future intent.
- `.aide/toolchain.lock`: minimal Contract/Profile lock record. It should include AIDE profile contract version, queue policy version if known, generated-artifact status, and Harness status as planned or not yet implemented.
- `.aide/components/catalog.yaml`: minimal component declarations for `core-contract`, `core-harness`, `core-compat`, `core-control`, `core-runtime-deferred`, `core-sdk-deferred`, `hosts-deferred`, `bridges-dominium`, `docs`, and `queue`.
- `.aide/commands/catalog.yaml`: declarative command catalog for implemented queue scripts and planned Harness commands.
- `.aide/policies/ownership.yaml`: path ownership and allowed-reference policy for the Profile.
- `.aide/policies/generated-artifacts.yaml`: source-of-truth and drift policy for generated outputs, with Q05 as the planned implementation point.
- `.aide/policies/compatibility.yaml`: profile-level compatibility policy pointer that does not replace bootstrap-era governance or matrices.
- `.aide/policies/validation-severity.yaml`: severity levels for future Contract/Harness validation findings.
- `.aide/tasks/catalog.yaml`: task type/catalog declarations for Q00 through Q08 and reusable queue task classes. It must not duplicate queue status as source of truth.
- `.aide/evals/catalog.yaml`: minimal eval declarations for documentation sanity, queue integrity, profile completeness, future Harness smoke, and future Compatibility smoke.
- `.aide/adapters/catalog.yaml`: metadata-only target adapter declarations for `codex`, `claude-code`, `openhands`, and `generic-agents`.
- `.aide/compat/schema-version.yaml`: Contract/Profile schema version record.
- `.aide/compat/migration-baseline.yaml`: migration baseline placeholder with no migration engine.
- `.aide/compat/README.md`: short explanation of compatibility records and Q06 relationship if useful.

The implementation should prefer one compact catalog file per declaration family unless a future worker finds a clear readability reason for one-file-per-record declarations. Do not create broad product architecture under `.aide/`.

## Schema Strategy

Q03 should define v0 shapes under `core/contract/**` without introducing executable validation. The preferred strategy is:

- Use human-readable YAML records for `.aide/` declarations because the existing queue and profile already use YAML.
- Define documented YAML shapes in `core/contract/README.md` and, if useful, in `core/contract/schemas/README.md`.
- Keep records within a JSON-compatible YAML subset where practical: maps, lists, strings, booleans, and simple scalar values.
- Defer full JSON Schema enforcement unless Q03 implementation creates small readable schema documents that do not require external dependencies.
- Record that Python standard library has no YAML or JSON Schema parser, so Q04 Harness validation must either use a conservative line/shape parser, accept JSON-compatible records through a small reader, or deliberately review a dependency decision later.

Planned schema or documented-shape topics:

- profile shape
- component declaration shape
- command declaration shape
- policy declaration shape
- task catalog shape
- eval declaration shape
- adapter declaration shape
- toolchain lock shape
- compatibility version and migration placeholder shape

## Source-Of-Truth Rules

Q03 should create `docs/reference/source-of-truth.md` and keep these rules explicit:

- `.aide/profile.yaml` and declaration catalogs under `.aide/` are canonical for the AIDE repo Profile/Contract.
- `.aide/queue/**` is canonical for task execution state, queue order, prompts, status, and evidence.
- `.aide/policies/**` is canonical for self-hosting autonomy, bypass, review gates, ownership, generated-artifact posture, compatibility posture, and validation severity once Q03 adds those policy records.
- `docs/**` contains human references and explanations; it should link to canonical records rather than replacing them.
- Bootstrap-era docs, specs, phase logs, host proofs, eval reports, matrices, inventory, environments, and packaging records remain historical evidence and compatibility inputs.
- Generated downstream artifacts are outputs, not source of truth, until a future reviewed policy says otherwise.
- Runtime caches, worker state, local IDE extension state, and chat history are not source of truth.

## Planned Deliverables

Q03 implementation should create or update:

- `.aide/profile.yaml`
- `.aide/toolchain.lock`
- `.aide/components/catalog.yaml`
- `.aide/commands/catalog.yaml`
- `.aide/policies/ownership.yaml`
- `.aide/policies/generated-artifacts.yaml`
- `.aide/policies/compatibility.yaml`
- `.aide/policies/validation-severity.yaml`
- `.aide/tasks/catalog.yaml`
- `.aide/evals/catalog.yaml`
- `.aide/adapters/catalog.yaml`
- `.aide/compat/schema-version.yaml`
- `.aide/compat/migration-baseline.yaml`
- `.aide/compat/README.md` if useful
- `core/contract/README.md`
- optional `core/contract/schemas/README.md` or minimal schema docs if the implementation keeps them readable and dependency-free
- `docs/reference/profile-contract-v0.md`
- `docs/reference/source-of-truth.md`
- minimal root doc updates to `README.md`, `DOCUMENTATION.md`, `ROADMAP.md`, `PLANS.md`, and `IMPLEMENT.md`
- minimal `AGENTS.md` and `.agents/skills/**` updates only if needed to point agents to the Profile/Contract after it exists
- Q03 evidence:
  - `.aide/queue/Q03-profile-contract-v0/evidence/changed-files.md`
  - `.aide/queue/Q03-profile-contract-v0/evidence/validation.md`
  - `.aide/queue/Q03-profile-contract-v0/evidence/profile-shape.md`
  - `.aide/queue/Q03-profile-contract-v0/evidence/remaining-risks.md`

## Milestones

1. Verify Q00, Q01, and Q02 status, outputs, review posture, and evidence.
2. Read existing `.aide/profile.yaml`, `.aide/toolchain.lock`, `.aide/policies/**`, `.aide/queue/**`, `core/contract/README.md`, and root docs.
3. Update Q03 status to `running` only after checking allowed paths and dependencies.
4. Define the minimal Profile/Contract v0 shape and source-of-truth rules.
5. Update `.aide/profile.yaml` and `.aide/toolchain.lock` honestly from P15 scaffold into Contract v0.
6. Add compact declaration catalogs under `.aide/components/`, `.aide/commands/`, `.aide/tasks/`, `.aide/evals/`, `.aide/adapters/`, and `.aide/compat/`.
7. Add or normalize Profile-level policies without loosening existing policies.
8. Update `core/contract/README.md` and optional schema notes.
9. Add `docs/reference/profile-contract-v0.md` and `docs/reference/source-of-truth.md`.
10. Update root docs and agent guidance only enough to point at the Contract v0.
11. Write Q03 evidence.
12. Run validation, allowed-path audit, terminology searches, and queue helper checks.
13. Move Q03 status to `needs_review` if complete, or `blocked` with evidence if not.

## Progress

- 2026-04-29: Q03 plan-only packet created. No Q03 implementation work, final `.aide/` contract changes, schemas, Harness commands, generated artifacts, Runtime, Hosts, Bridges, provider adapters, or source refactors were performed.
- 2026-04-29: Plan-only validation completed and recorded in `evidence/planning-validation.md`.
- 2026-04-29: Q03 implementation started with explicit human authorization while Q00, Q01, and Q02 remain `needs_review`.
- 2026-04-29: Q03 status moved to `running`; queue index moved Q03 to implementation state.
- 2026-04-29: Refined `.aide/profile.yaml` and `.aide/toolchain.lock` into Contract/Profile v0 records.
- 2026-04-29: Added compact declaration catalogs for components, commands, tasks, evals, adapters, and compatibility.
- 2026-04-29: Added Profile-level ownership, generated-artifact, compatibility, and validation-severity policies without modifying autonomy, bypass, or review-gate policy files.
- 2026-04-29: Added documented Contract v0 shapes under `core/contract/shapes/`.
- 2026-04-29: Added `docs/reference/profile-contract-v0.md` and `docs/reference/source-of-truth.md`.
- 2026-04-29: Updated root docs, `AGENTS.md`, and the AIDE queue skill with minimal Profile/Contract pointers.

## Surprises And Discoveries

- 2026-04-29: Q00, Q01, and Q02 are implemented but still `needs_review`; Q03 implementation should require explicit human authorization or accepted prior reviews before editing the Profile/Contract.
- 2026-04-29: `.aide/profile.yaml` and `.aide/toolchain.lock` already exist from P15 as minimal bootstrap scaffold files. Q03 should refine them rather than blindly overwriting.
- 2026-04-29: `.aide/policies/autonomy.yaml`, `.aide/policies/bypass.yaml`, and `.aide/policies/review-gates.yaml` already define important self-hosting constraints and must not be loosened by Q03.
- 2026-04-29: The user prompt requested one YAML file per component unless the ExecPlan chose another pattern; the ExecPlan chose compact catalogs, so Q03 kept a single component catalog and validated required component ids inside it.
- 2026-04-29: Existing queue scripts are useful for status and next-item checks, but they intentionally remain read-only queue helpers and are not Harness v0.

## Decision Log

- 2026-04-29: Q03 planning uses `status: pending` because `planning_complete` is not an allowed queue-policy task state. `planning_state: planning_complete` records that the plan is ready.
- 2026-04-29: The planned v0 contract uses compact YAML catalogs under `.aide/` rather than a broad file-per-record tree, keeping v0 small and reviewable.
- 2026-04-29: Q03 should use documented YAML shapes first and avoid external validation dependencies. Full Harness behavior belongs to Q04.
- 2026-04-29: Generated downstream artifacts remain deferred to Q05. Q03 may define their policy boundary but must not create them.
- 2026-04-29: Q03 added new Profile-level policy files but did not edit `autonomy.yaml`, `bypass.yaml`, or `review-gates.yaml`. The stricter existing policy wins on conflict.
- 2026-04-29: Adapter declarations are metadata-only and provider-neutral; generated downstream artifacts remain Q05.

## Validation And Acceptance

This plan-only task is acceptable when:

- `.aide/queue/Q03-profile-contract-v0/task.yaml` exists.
- `.aide/queue/Q03-profile-contract-v0/ExecPlan.md` exists and contains all required sections.
- `.aide/queue/Q03-profile-contract-v0/prompt.md` exists.
- `.aide/queue/Q03-profile-contract-v0/status.yaml` exists.
- `.aide/queue/Q03-profile-contract-v0/evidence/planning-validation.md` exists.
- `.aide/queue/index.yaml` references the Q03 task, ExecPlan, prompt, and evidence path.
- `PLANS.md` contains only a minimal Q03 planning pointer if updated.
- No final Contract/Profile implementation, schemas, generated artifacts, Harness commands, source refactors, or forbidden paths are modified.

Plan-only validation completed on 2026-04-29:

- Required Q03 queue planning files exist.
- Queue helper scripts run and identify Q03 as the next pending item.
- `.aide/queue/index.yaml` references Q03 task, ExecPlan, prompt, and evidence paths.
- Required ExecPlan sections are present.
- `git diff --check` passed with line-ending normalization warnings only.
- Allowed-path and final-contract-path audits passed.

Q03 implementation will be acceptable only when:

- Required `.aide/` Profile/Contract files exist and are status-labeled.
- Profile and Harness are clearly distinguished.
- Existing policies are preserved and not loosened.
- `core/contract/**` documents the v0 contract shape without implementing Harness behavior.
- Source-of-truth rules and profile reference docs exist.
- Root docs and agent guidance point to the new contract without marketing language or overstated implementation claims.
- Evidence records commands, results, changed files, profile shape, and remaining risks.
- Q03 status moves to `needs_review` or `blocked` honestly.

Implementation validation was run on 2026-04-29 and recorded in `evidence/validation.md`.

## Idempotence And Recovery

A stateless worker can restart Q03 by reading:

- `AGENTS.md`
- `.aide/queue/policy.yaml`
- `.aide/queue/index.yaml`
- Q00 status, ExecPlan, evidence, and outputs
- Q01 status, ExecPlan, evidence, charters, decisions, and documentation maps
- Q02 status, ExecPlan, evidence, skeleton READMEs, and structural migration map
- `.aide/queue/Q03-profile-contract-v0/task.yaml`
- `.aide/queue/Q03-profile-contract-v0/ExecPlan.md`
- `.aide/queue/Q03-profile-contract-v0/status.yaml`

If partial Q03 implementation already exists, inspect `git status`, `git diff`, Q03 evidence, and queue status before editing. Preserve unrelated user changes. If final `.aide/` contract files or `core/contract/**` schemas were changed before an implementation task, determine whether they are Q03-owned and review-gated; if not, stop and record a blocker. If forbidden paths were modified, stop and record a blocker. Re-run validation after any correction.

## Evidence To Produce

Q03 implementation should produce:

- `.aide/queue/Q03-profile-contract-v0/evidence/changed-files.md`
- `.aide/queue/Q03-profile-contract-v0/evidence/validation.md`
- `.aide/queue/Q03-profile-contract-v0/evidence/profile-shape.md`
- `.aide/queue/Q03-profile-contract-v0/evidence/remaining-risks.md`
- `.aide/queue/Q03-profile-contract-v0/evidence/blocker.md` if blocked

The plan-only task produces:

- `.aide/queue/Q03-profile-contract-v0/evidence/planning-validation.md`

## Outcomes And Retrospective

- Q03 implemented the minimal declarative Profile/Contract v0 and is awaiting review.
- Q03 did not implement Harness commands, generated downstream artifacts, source refactors, Runtime, Hosts, Bridges, provider adapters, app surfaces, or autonomous service logic.
- Q03 kept bootstrap-era records in place and documented source-of-truth boundaries for future work.
