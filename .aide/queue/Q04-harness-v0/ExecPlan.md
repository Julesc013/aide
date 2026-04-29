# Q04 ExecPlan: Harness v0

## Purpose

Q04 will implement the smallest executable AIDE Harness v0 command surface. The future implementation should read the Q03 `.aide/` Profile/Contract v0, perform basic deterministic validation and doctoring, and provide stable local command entrypoints from the repository root.

Q04 is not the generated artifact step, not the compatibility baseline, not the Dominium Bridge baseline, and not Runtime, Hosts, Commander, Mobile, IDE extension, provider, app, or autonomous service work. It must keep the Q03 distinction intact:

- Profile / Contract: declarative repo truth.
- Harness: executable machinery that imports, compiles, validates, doctors, migrates, and bakeoffs that repo truth.
- Generated downstream artifacts: Q05.
- Compatibility baseline: Q06.
- Dominium Bridge baseline: Q07.
- Runtime, Service, Hosts, SDK, and automation: later reviewed queue work.

## Background And Current Repo Context

AIDE is being rebooted in place. Bootstrap-era records, source files, host proof lanes, eval reports, packaging records, environments, labs, and evidence remain historical baseline and compatibility inputs.

Facts verified during Q04 planning:

- Q00, Q01, Q02, and Q03 exist and currently have `status: needs_review`.
- Q00 produced baseline reboot records: bootstrap-era constitution, reboot charter, repo census, and reboot roadmap.
- Q01 produced documentation families, architecture charters, decision records, terminology references, and documentation migration mapping.
- Q02 produced README-only skeletons for `core/`, target host categories, `bridges/`, Dominium Bridge, and `docs/reference/structural-migration-map.md`.
- Q03 produced declarative Profile/Contract v0 records under `.aide/`, documented shapes under `core/contract/shapes/**`, and source-of-truth references.
- `.aide/commands/catalog.yaml` declares queue helper scripts as implemented and future Harness commands as planned.
- `core/harness/README.md` is skeleton-only and explicitly says Harness v0 is Q04.
- `scripts/aide-queue-status`, `scripts/aide-queue-next`, and `scripts/aide-queue-run` are conservative queue helpers. They are not Harness v0.
- Python standard library does not include YAML or JSON Schema parsing, and Q03 intentionally used documented YAML shapes rather than executable schema enforcement.

Because upstream queue items remain review-gated, a future Q04 implementation worker should proceed only if prior Q00 through Q03 outputs have been reviewed and accepted or the human prompt explicitly authorizes Q04 implementation while acknowledging the open review gates.

## Scope

Q04 implementation should add a minimal local Harness that can:

- expose a repo-root `aide` command entrypoint;
- read and structurally inspect the Q03 `.aide/` contract records;
- validate required files, directories, required field anchors, queue metadata, and source-of-truth references;
- report diagnostics with stable severities;
- produce an actionable doctor report;
- produce a compile plan/report without writing generated downstream artifacts;
- report no-op baseline migration status;
- report bakeoff readiness without calling providers, models, native tools, or host environments;
- add lightweight standard-library smoke tests and documentation.

## Non-goals

- Do not implement Q05 generated downstream artifacts.
- Do not create `CLAUDE.md`, `.claude/**`, final generated `.agents/skills/*` outputs, provider files, IDE extension files, package manifests, or app surfaces.
- Do not implement Q06 compatibility baseline, migration engine, replay corpus, or schema upgrade system.
- Do not implement Q07 Dominium Bridge behavior or broaden XStack beyond Dominium-local proof posture.
- Do not implement Runtime, broker, scheduler, router, context service, patch engine, approval engine, workers, transport, service host, Commander, Mobile, IDE extension, provider/model integration, release automation, or autonomous worker invocation.
- Do not migrate the bootstrap-era `shared/**` implementation or existing host proof lanes.
- Do not replace queue policy, autonomy policy, bypass policy, review gates, governance, support tiers, or capability levels.
- Do not pretend full YAML or JSON Schema validation exists if Q04 only implements structural checks.

## Allowed Paths For Q04 Implementation

- `core/harness/**`
- `core/contract/**` only for read-only-compatible helpers or docs required by the Harness
- `scripts/aide`
- `scripts/**` only for small wrappers or test helpers directly needed for Harness v0
- `docs/reference/harness-v0.md`
- `docs/reference/profile-contract-v0.md` only if needed to clarify what Q04 validates
- `README.md`
- `DOCUMENTATION.md`
- `ROADMAP.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `.aide/queue/Q04-harness-v0/**`
- `.aide/queue/index.yaml`

## Forbidden Paths For Q04 Implementation

- `shared/**`
- existing `hosts/**` implementation/proof files
- `bridges/**`
- `core/runtime/**`
- `core/compat/**` except conceptual docs references if needed
- `core/control/**` except conceptual docs references if needed
- `core/sdk/**`
- `governance/**`
- `inventory/**`
- `matrices/**`
- `research/**`
- `specs/**`
- `environments/**`
- `labs/**`
- `evals/**`
- `packaging/**`
- generated downstream artifacts such as `CLAUDE.md`, `.claude/**`, or final generated `.agents/skills/*` target outputs
- provider/model integrations
- runtime, broker, service, worker, app, IDE, extension, or host implementation code

## Harness Command Model

Q04 should implement a small command surface under one repo-root command:

- `aide init`: minimal scaffold report. It should support dry-run behavior, detect existing `.aide/`, and refuse to overwrite existing contract files. Full init or upgrade behavior may remain stubbed with honest messaging.
- `aide import`: report-only importer. It may inspect existing repo guidance surfaces and report candidate imports, but it must not rewrite the Profile destructively in Q04.
- `aide compile`: deterministic compile plan. It should read `.aide/`, check contract readability, and print what Q05 would later generate. It must not emit final downstream artifacts.
- `aide validate`: primary Q04 command. It should check required `.aide/` files, profile/toolchain anchors, required declaration catalogs, compatibility placeholders, queue packet coherence, and source-of-truth docs. It should return nonzero when any error diagnostics are present.
- `aide doctor`: human-readable diagnostics and repair hints. It should explain missing setup, inconsistent queue metadata, planned but unimplemented Harness pieces, stale/missing evidence, and next recommended steps.
- `aide migrate`: no-op baseline migration report. It should read current contract version and `.aide/compat/**` placeholders, then report whether migration is needed without implementing a migration engine.
- `aide bakeoff`: metadata-only bakeoff readiness report. It should read declared eval metadata if present and report that no executable bakeoff scenarios exist yet unless Q04 adds local smoke scenarios. It must not call models, providers, network tools, or native host environments.

Recommended command invocation examples:

```powershell
py -3 scripts/aide --help
py -3 scripts/aide validate
py -3 scripts/aide doctor
py -3 scripts/aide compile
py -3 scripts/aide migrate
py -3 scripts/aide bakeoff
```

The command catalog in `.aide/commands/catalog.yaml` may be updated by Q04 implementation only if necessary to mark the new Harness command posture truthfully.

## Contract Loading Strategy

Q04 should use Python standard library only.

Because Python standard library has no YAML parser, Q04 should not claim full YAML validation. The preferred v0 strategy is:

- load known required files as UTF-8 text;
- perform required path checks;
- use a tiny restricted reader only for simple line-oriented anchors needed by v0, such as top-level `key: value` pairs and list item `- id:` entries;
- treat nested semantic validation as structural anchor checks unless a later reviewed task authorizes a stronger parser;
- preserve deterministic diagnostics for unreadable, missing, or malformed-enough records.

Suggested implementation files:

- `scripts/aide`: small Python wrapper runnable from the repo root.
- `core/harness/aide_harness.py`: main CLI dispatcher or module entrypoint.
- `core/harness/commands.py`: command handlers.
- `core/harness/contract_loader.py`: restricted file/path/text reader.
- `core/harness/diagnostics.py`: diagnostic model and formatting.

The future worker may choose fewer files if that keeps v0 simpler, but it should avoid putting all behavior into the wrapper script.

## Validation Severity Model

Use the Q03 severity vocabulary and keep behavior explicit:

- `info`: advisory observation, never blocks.
- `warning`: should be reviewed or tracked, does not make the command fail by itself.
- `error`: hard validation failure; `aide validate` must return nonzero.

The Q03 policy also defines `blocker`. In Q04, `blocker` should be reserved for queue/policy/safety situations that require stopping work and recording evidence, not for ordinary missing-file validation output unless the policy gate itself is reached.

Diagnostics should include:

- stable code;
- severity;
- message;
- optional path;
- optional hint.

## Compile/Report Boundary

Q04 compile is not Q05 generation.

`aide compile` should print a deterministic compile plan or report to stdout. It may say which future downstream artifacts would be candidates after Q05, but it must not create `CLAUDE.md`, `.claude/**`, provider files, generated skills, package manifests, app files, or other generated outputs.

If the implementation needs a file output for tests or evidence, it should write only task-local evidence during the Q04 queue item, not canonical generated target files. The default command behavior should remain non-mutating.

## Migration Boundary

`aide migrate` should read the current contract/profile version and compatibility placeholders, then report one of:

- current baseline, no migration needed;
- migration needed, but migration engine is not implemented;
- migration status cannot be determined because required records are missing or unreadable.

It must not alter `.aide/**`, move files, rewrite schemas, or implement Q06.

## Bakeoff Boundary

`aide bakeoff` should read `.aide/evals/catalog.yaml` if present and report declared bakeoff or eval readiness. Q04 should not call model providers, external services, native host tools, IDEs, package managers, or network resources.

If no executable bakeoff scenarios exist, the honest successful output is a structured "no executable bakeoff scenarios yet" status.

## Planned Deliverables

Q04 implementation should create or update:

- `scripts/aide`
- `core/harness/README.md`
- `core/harness/aide_harness.py`
- `core/harness/commands.py`
- `core/harness/contract_loader.py`
- `core/harness/diagnostics.py`
- optional `core/harness/tests/**` standard-library smoke tests, if kept small
- `docs/reference/harness-v0.md`
- `docs/reference/profile-contract-v0.md` only if validation boundary clarification is needed
- minimal root doc updates to `README.md`, `DOCUMENTATION.md`, `ROADMAP.md`, `PLANS.md`, and `IMPLEMENT.md`
- `.aide/queue/Q04-harness-v0/status.yaml`
- `.aide/queue/Q04-harness-v0/evidence/changed-files.md`
- `.aide/queue/Q04-harness-v0/evidence/validation.md`
- `.aide/queue/Q04-harness-v0/evidence/command-smoke.md`
- `.aide/queue/Q04-harness-v0/evidence/remaining-risks.md`

Q04 implementation may update `.aide/queue/index.yaml` and `.aide/commands/catalog.yaml` if needed to record truthful Harness status, but it must not loosen policy or implement generated artifacts.

## Milestones

1. Verify Q00 through Q03 status, outputs, review posture, and evidence.
2. Read Q04 task packet, this ExecPlan, queue policy, Q03 contract records, and root docs.
3. Confirm allowed paths and start Q04 status only after dependency posture is acknowledged.
4. Add the minimal Harness implementation files and repo-root `scripts/aide` wrapper.
5. Implement deterministic command handlers for help, init, import, compile, validate, doctor, migrate, and bakeoff.
6. Implement restricted contract loading and diagnostic formatting.
7. Add lightweight standard-library smoke tests if practical.
8. Add `docs/reference/harness-v0.md` and update `core/harness/README.md`.
9. Update root docs and Q04 queue status/evidence.
10. Run command smoke checks, validation, queue helper checks, terminology scans, `git diff --check`, and an allowed-path audit.
11. Stop at `needs_review` if complete, or `blocked` with blocker evidence if not.

## Progress

- 2026-04-29: Q04 plan-only packet created. No Harness implementation files, command entrypoints, generated artifacts, source moves, Runtime, Hosts, Bridges, provider integrations, or app surfaces were created.

## Surprises And Discoveries

- 2026-04-29: Q00, Q01, Q02, and Q03 are all implemented but still `needs_review`, so Q04 implementation must treat them as review-gated dependencies unless explicitly authorized by a future prompt.
- 2026-04-29: Q03 already records future Harness commands in `.aide/commands/catalog.yaml`, but they are `planned`; Q04 can update that posture only when implementation actually exists.
- 2026-04-29: Existing queue helper scripts duplicate a small line-oriented queue parser. Q04 should avoid overbuilding a general parser and may share a similarly restricted approach for v0 contract checks.
- 2026-04-29: The Q03 Contract shape deliberately avoids external dependencies, so Q04 should not introduce PyYAML or JSON Schema dependencies without a separate reviewed dependency decision.

## Decision Log

- 2026-04-29: Q04 planning uses `status: pending` plus `planning_state: planning_complete` because `planning_complete` is not a queue-policy task state.
- 2026-04-29: The planned entrypoint is `scripts/aide`, with implementation under `core/harness/**`, so the command is runnable from repo root while Harness logic stays in Core.
- 2026-04-29: Q04 should use Python standard library only and restricted structural checks instead of full YAML/schema validation.
- 2026-04-29: `aide validate` is the primary command and should be the only one that must fail nonzero on hard contract errors by default.
- 2026-04-29: `aide compile` is a compile-plan/report command only. Q05 owns generated downstream target files.
- 2026-04-29: `aide migrate` is a no-op baseline report only. Q06 owns compatibility baseline and migration hardening.
- 2026-04-29: `aide bakeoff` is metadata/report-only in Q04 and must not call models, providers, tools, or native hosts.

## Validation And Acceptance

This plan-only task is acceptable when:

- `.aide/queue/Q04-harness-v0/task.yaml` exists.
- `.aide/queue/Q04-harness-v0/ExecPlan.md` exists and contains all required sections.
- `.aide/queue/Q04-harness-v0/prompt.md` exists.
- `.aide/queue/Q04-harness-v0/status.yaml` exists.
- `.aide/queue/Q04-harness-v0/evidence/planning-validation.md` exists.
- `.aide/queue/index.yaml` references the Q04 task, ExecPlan, prompt, and evidence path.
- `PLANS.md` contains only a minimal Q04 planning pointer if updated.
- No Harness implementation, command entrypoint, generated artifact, source refactor, Runtime, Host, Bridge, provider, app, or Q05+ work is created.

Q04 implementation will be acceptable only when:

- The Harness command entrypoint runs from the repo root using Python standard library only.
- Required commands exist with honest behavior and messaging.
- `aide validate` checks Q03 contract posture and queue coherence and returns nonzero on hard failures.
- `aide doctor`, `aide compile`, `aide migrate`, and `aide bakeoff` are deterministic and non-mutating by default.
- Generated downstream artifacts are not created.
- Evidence records command smoke output, validation, changed files, and remaining risks.
- Q04 status moves to `needs_review` or `blocked` honestly.

Plan-only validation is recorded in `evidence/planning-validation.md`.

## Idempotence And Recovery

A stateless worker can restart Q04 by reading:

- `AGENTS.md`
- `.aide/queue/policy.yaml`
- `.aide/queue/index.yaml`
- Q00, Q01, Q02, and Q03 status files, ExecPlans, evidence, and outputs
- `.aide/profile.yaml`
- `.aide/toolchain.lock`
- `.aide/commands/catalog.yaml`
- `.aide/evals/catalog.yaml`
- `.aide/compat/**`
- `core/contract/README.md`
- `core/harness/README.md`
- `docs/reference/profile-contract-v0.md`
- `docs/reference/source-of-truth.md`
- `.aide/queue/Q04-harness-v0/task.yaml`
- `.aide/queue/Q04-harness-v0/ExecPlan.md`
- `.aide/queue/Q04-harness-v0/status.yaml`

If partial Q04 implementation already exists, inspect `git status`, `git diff`, Q04 evidence, and queue status before editing. Preserve unrelated user changes. If command files, Harness files, or docs were created before the implementation task, determine whether they are Q04-owned. If forbidden paths were modified, stop and record a blocker. If generated downstream artifacts were created, stop and record a review-gate violation unless a future prompt explicitly authorized Q05.

## Evidence To Produce

Q04 implementation should produce:

- `.aide/queue/Q04-harness-v0/evidence/changed-files.md`
- `.aide/queue/Q04-harness-v0/evidence/validation.md`
- `.aide/queue/Q04-harness-v0/evidence/command-smoke.md`
- `.aide/queue/Q04-harness-v0/evidence/remaining-risks.md`
- `.aide/queue/Q04-harness-v0/evidence/blocker.md` if blocked

The plan-only task produces:

- `.aide/queue/Q04-harness-v0/evidence/planning-validation.md`

## Outcomes And Retrospective

- Pending future Q04 implementation.
- No implementation work has been performed by this plan-only task.
- Main known risk: prior Q00 through Q03 outputs remain `needs_review`; Q04 implementation must not treat them as accepted without review or explicit authorization.
