# Q05 ExecPlan: Generated Artifacts v0

## Purpose

Q05 will implement the first deterministic generated downstream artifact pipeline for the AIDE self-hosting reboot. The implementation should let agents consume current AIDE repo intelligence through managed or preview outputs while preserving the canonical source-of-truth model:

- `.aide/` is the canonical Profile/Contract.
- `.aide/queue/` is the canonical execution queue.
- generated downstream artifacts are compiled or managed outputs, not canonical truth.
- Harness validates before and after generation.

Q05 is not Q06 Compatibility, Q07 Dominium Bridge, Runtime, Hosts, Commander, Mobile, IDE extension, provider adapter, app surface, release automation, or autonomous service logic.

## Background And Current Repo Context

AIDE is being rebooted in place. Bootstrap-era records, source files, host proof lanes, eval records, packaging records, environment records, and evidence remain historical baseline and must not be moved or erased by Q05.

Current facts verified during Q05 planning:

- Q04 Harness v0 has passed review with outcome `PASS_WITH_NOTES`.
- `scripts/aide` exists and exposes `init`, `import`, `compile`, `validate`, `doctor`, `migrate`, and `bakeoff`.
- `py -3 scripts/aide validate`, `doctor`, and `compile` pass with warnings only.
- `aide compile` currently prints a compile plan and creates no final generated artifacts.
- `CLAUDE.md` and `.claude/` are absent.
- `.aide/profile.yaml`, `.aide/toolchain.lock`, and `.aide/commands/catalog.yaml` still contain Q03-era Harness planned/not-implemented wording.
- Harness v0 reports those stale records as warnings.
- Q00 through Q03 remain `needs_review`; foundation review accepted them with notes and Q04 review says Q05 planning may proceed.

The future Q05 worker must re-verify these facts before implementation.

## Scope

Q05 implementation should:

- perform a bounded pre-generation metadata refresh for Q03-era Harness wording;
- define generated artifact v0 policy in human docs;
- add deterministic generation support to Harness compile behavior;
- add generated artifact validation and stale-output detection to Harness validate behavior;
- create a generated artifact manifest under `.aide/generated/**`;
- create or update only the target artifacts approved by this plan;
- write task-local evidence and stop at review.

## Non-goals

- Do not make generated downstream artifacts canonical truth.
- Do not silently overwrite human-maintained files.
- Do not fully regenerate `AGENTS.md`.
- Do not fully regenerate existing `.agents/skills/**`.
- Do not create unsafe Claude hooks.
- Do not define autonomous agents that bypass AIDE queue policy.
- Do not implement full Compatibility baseline, migration engine, or replay corpus.
- Do not implement Dominium Bridge behavior.
- Do not build Runtime, broker, service, Commander, Mobile, IDE extensions, provider/model integrations, browser bridges, web portals, app surfaces, packaging, release automation, or autonomous service logic.
- Do not move or refactor bootstrap-era source code.
- Do not overfit the generated artifact model to Claude Code or Codex.

## Allowed Paths For Q05 Implementation

- `core/harness/**`
- `core/contract/**` only if needed for generated-artifact metadata or helper docs
- `.aide/generated/**`
- `.aide/adapters/**` only if needed for target metadata
- `.aide/commands/**` only for compile/validate target support and bounded Harness-status refresh
- `.aide/evals/**` only for generated-artifact validation declarations
- `.aide/profile.yaml` only for bounded Harness-status refresh
- `.aide/toolchain.lock` only for bounded Harness-status refresh
- `AGENTS.md`
- `.agents/skills/**`
- `CLAUDE.md` only if this target policy is changed by reviewed evidence during Q05 implementation
- `.claude/**` only if this target policy is changed by reviewed evidence during Q05 implementation
- `docs/reference/generated-artifacts-v0.md`
- `docs/reference/source-of-truth.md`
- `docs/reference/harness-v0.md`
- `README.md`
- `DOCUMENTATION.md`
- `ROADMAP.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `.aide/queue/Q05-generated-artifacts-v0/**`
- `.aide/queue/index.yaml`

## Forbidden Paths For Q05 Implementation

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
- `evals/**` except specifically allowed AIDE generated-artifact eval declarations under `.aide/evals/**`
- `packaging/**`
- provider/model integrations
- web search integrations
- local model integrations
- runtime/broker/service code
- IDE/app/host code
- release/package automation
- Q06/Q07/Q08 implementation

## Generated Artifact Model

Generated artifacts are deterministic outputs compiled from canonical source inputs. For Q05 v0, generated artifacts may be:

- managed sections inside existing human-maintained files;
- preview files under `.aide/generated/preview/**`;
- manifest records under `.aide/generated/**`.

Generated artifacts must be:

- deterministic for the same source inputs;
- clearly marked with provenance;
- reviewable in Git diffs;
- recoverable if generation would overwrite manual content;
- validated before and after generation.

Generated artifacts must not be:

- canonical product doctrine;
- hidden caches;
- runtime state;
- release artifacts;
- provider/model integrations;
- permission to bypass `.aide/queue/`.

## Source-Of-Truth Rules

- `.aide/profile.yaml` and declaration catalogs under `.aide/` are canonical for the self-hosting Profile/Contract.
- `.aide/queue/**` is canonical for queue execution state, task packets, status, prompts, ExecPlans, and evidence.
- `docs/**`, root docs, and `core/contract/**` provide human explanation and references.
- Bootstrap-era docs, specs, source files, host proofs, eval reports, matrices, inventory, environments, labs, and packaging records remain historical evidence and compatibility inputs.
- Generated downstream artifacts are compiled or managed outputs and are not canonical unless a future reviewed policy explicitly changes that.
- Runtime caches, worker state, local IDE state, extension task queues, and chat history are not truth.

## Target Artifact Policy

| Target | Q05 v0 mode | Rationale |
| --- | --- | --- |
| `AGENTS.md` | managed-section generated | Preserve root operating law while adding a deterministic AIDE contract/queue summary section. Never full-file overwrite in Q05. |
| `.agents/skills/aide-queue/SKILL.md` | managed-section generated | Existing skill remains human-maintained; Q05 may add or refresh a bounded generated source-of-truth summary. |
| `.agents/skills/aide-execplan/SKILL.md` | managed-section generated | Existing skill remains human-maintained; Q05 may add or refresh a bounded generated ExecPlan/queue summary. |
| `.agents/skills/aide-review/SKILL.md` | managed-section generated | Existing skill remains human-maintained; Q05 may add or refresh a bounded generated review-gate summary. |
| future `.agents/skills/aide-contract/SKILL.md` | deferred | Do not create broad new skills in Q05 unless implementation evidence proves a small generated preview is needed. |
| future `.agents/skills/aide-harness/SKILL.md` | deferred | Defer until generated skill policy has review feedback. |
| future `.agents/skills/aide-generated-artifacts/SKILL.md` | deferred | Defer until Q05 itself is reviewed. |
| `CLAUDE.md` | generated preview only | Create preview under `.aide/generated/preview/CLAUDE.md`; do not create final root `CLAUDE.md` in Q05 v0 unless the worker records an explicit review-gate decision and keeps it generated with markers. |
| `.claude/settings.json` | deferred | Avoid hooks, auto-execution, or Claude-specific settings in Q05 v0. |
| `.claude/agents/*` | generated preview only | Optional previews under `.aide/generated/preview/.claude/agents/**`; final `.claude/**` remains deferred unless reviewed within Q05. |

## Managed-Section Strategy

Managed sections must use stable markers. Markdown files should use this format:

```md
<!-- AIDE-GENERATED:BEGIN section=<section-id> generator=aide-harness-v0 mode=managed-section sources=<comma-separated-paths> fingerprint=sha256:<hex> manual=outside-only -->
...
<!-- AIDE-GENERATED:END section=<section-id> -->
```

Rules:

- The start and end markers are required.
- The generated body may be replaced only by the Harness generator.
- Manual edits are allowed outside the marked section.
- Manual edits inside a marked section should be reported by `aide validate` as review-required or error, depending on target policy.
- Fingerprints should be stable hashes of normalized source content and generated body inputs.
- Avoid timestamps inside generated files.

JSON preview files should use a deterministic top-level metadata object where valid for the target shape, or remain preview-only Markdown if target JSON shape would be compromised.

## Manifest Strategy

Q05 should create `.aide/generated/manifest.yaml`.

The manifest should record:

- schema version;
- generator name and version;
- source input paths;
- target path;
- generation mode;
- manual edit policy;
- marker style;
- source fingerprint;
- generated content fingerprint;
- target status: `managed`, `preview`, `deferred`, or `blocked`;
- validation command expectations.

Prefer fingerprints over timestamps. If a generation id is needed, derive it deterministically from source fingerprints rather than wall-clock time.

The manifest describes generated output state. It is not a replacement for `.aide/profile.yaml`, `.aide/queue/**`, or source docs.

## Stale-Output Detection Strategy

Q05 should update Harness validation so it can:

- read `.aide/generated/manifest.yaml`;
- verify each required target exists according to mode;
- verify markers exist and match the manifest;
- recompute source fingerprints;
- detect stale generated content when source fingerprints or generated body fingerprints differ;
- detect missing preview files where preview mode is required;
- detect final files created without markers;
- detect manual edits inside generated regions;
- report missing/deferred targets according to target status.

Severity guidance:

- `error`: missing required generated target, markerless generated full file, unauthorized manual edit inside managed section, or final generated file with no manifest entry.
- `warning`: stale preview, deferred optional target, Q03-era records not yet refreshed when generation is not being written.
- `info`: generated target present and current, deferred target intentionally absent, preview current.
- `review_required`: use the existing warning model in Q05 v0 unless a separate severity is added by a reviewed policy.

## Harness Compile/Validate Changes

Q05 should update `aide compile` carefully:

- default behavior remains non-mutating and prints a deterministic plan;
- add `--dry-run` as explicit non-mutating behavior;
- add `--preview` to write preview outputs under `.aide/generated/preview/**` only;
- add `--write` to update approved managed sections and manifest entries only after validation passes;
- report exact files that would change;
- refuse destructive overwrite when a target lacks expected markers;
- refuse final `CLAUDE.md` or `.claude/**` output unless the target policy has been explicitly changed and recorded in Q05 evidence.

Q05 should update `aide validate` so it checks generated artifact markers, manifest coherence, stale fingerprints, and unauthorized edits. It should still return nonzero on hard errors.

## Q03-Era Harness Wording Decision

Decision: Q05 implementation should include a bounded pre-generation metadata refresh before any generated output is written.

Reason:

- `.aide/profile.yaml`, `.aide/toolchain.lock`, and `.aide/commands/catalog.yaml` are canonical inputs for generated artifacts.
- These files still say Harness v0 is planned or not implemented.
- Generating agent-facing guidance from stale canonical records could produce misleading outputs.
- The refresh is small, factual, and directly tied to Q04 review outcome.

Allowed refresh only:

- mark Harness v0 as implemented/passed with notes where the current files refer to Q04 planned or not implemented;
- keep generated artifacts as Q05-owned and not implemented until Q05 completes;
- keep compatibility baseline as Q06, Dominium Bridge as Q07, and Runtime/Hosts as deferred;
- update command catalog posture for `aide init`, `import`, `compile`, `validate`, `doctor`, `migrate`, and `bakeoff` to reflect Q04 reality;
- do not refactor the whole Contract/Profile.

If the future worker cannot keep this refresh bounded, it must stop and write a blocker or request a narrow QFIX.

## Planned Deliverables

Q05 implementation should create or update:

- bounded Harness-status refresh in `.aide/profile.yaml`;
- bounded Harness-status refresh in `.aide/toolchain.lock`;
- bounded Harness command posture refresh in `.aide/commands/catalog.yaml`;
- `.aide/generated/manifest.yaml`;
- `.aide/generated/preview/CLAUDE.md`;
- optional `.aide/generated/preview/.claude/agents/**` preview files if kept small and role-limited;
- managed sections in `AGENTS.md`;
- managed sections in `.agents/skills/aide-queue/SKILL.md`;
- managed sections in `.agents/skills/aide-execplan/SKILL.md`;
- managed sections in `.agents/skills/aide-review/SKILL.md`;
- Harness generator/manifest helpers under `core/harness/**`;
- Harness tests under `core/harness/tests/**`;
- `docs/reference/generated-artifacts-v0.md`;
- updates to `docs/reference/source-of-truth.md`;
- updates to `docs/reference/harness-v0.md`;
- minimal root doc updates to `README.md`, `DOCUMENTATION.md`, `ROADMAP.md`, `PLANS.md`, and `IMPLEMENT.md`;
- Q05 status and evidence under `.aide/queue/Q05-generated-artifacts-v0/**`.

Q05 implementation should not create final `CLAUDE.md`, final `.claude/settings.json`, or final `.claude/agents/**` unless the worker records a specific review-gate decision and keeps changes deterministic, marked, and non-canonical.

## Milestones

1. Re-read AGENTS, queue policy, Q04 review, foundation/full audit, Q00 through Q04 outputs, Q03 contract records, Q04 Harness files, root docs, and this Q05 packet.
2. Confirm Q04 remains `passed`; stop if not.
3. Run `py -3 scripts/aide validate`, `doctor`, and `compile` before edits.
4. Update Q05 status to `running` only after confirming allowed paths.
5. Perform the bounded Q03-era Harness wording refresh.
6. Add generated artifact manifest and marker policy docs.
7. Add Harness generated-artifact helpers and compile/validate changes.
8. Add managed sections/previews according to the target artifact policy.
9. Run compile dry-run/preview/write flows as authorized by the target policy.
10. Run post-generation validation, tests, queue helpers, generated artifact checks, `git diff --check`, and allowed-path audit.
11. Write Q05 evidence.
12. Stop at `needs_review` if complete, or `blocked` with blocker evidence if not.

## Progress

- 2026-04-30: Q05 plan-only packet created after Q04 review commit `12624d6 Review Q04 Harness v0`.
- 2026-04-30: Q05 planning decided that a bounded Q03-era Harness wording refresh is required before generated outputs are written.
- 2026-04-30: No Q05 implementation, final generated artifacts, Harness implementation edits, `.aide` contract edits, `AGENTS.md` edits, `.agents/skills/**` edits, `CLAUDE.md`, or `.claude/**` changes were made by this plan-only task.

## Surprises And Discoveries

- Q04 passed review, but `aide doctor` still says "Q04 should stop at needs_review" because that text is static in the Q04 implementation. This is not a planning blocker, but Q05 implementation may update doctor wording if it updates Harness diagnostics for generated artifacts.
- Q03-era Harness wording remains in canonical contract inputs. This is safe for planning but should be refreshed before generated outputs are written.
- `CLAUDE.md` and `.claude/` remain absent, which makes preview-first Claude planning straightforward.

## Decision Log

- 2026-04-30: Q05 planning keeps final generated artifacts non-canonical and requires deterministic markers plus a manifest.
- 2026-04-30: Q05 implementation should refresh stale Q03 Harness status wording before generation because those records are canonical inputs.
- 2026-04-30: `AGENTS.md` and existing `.agents/skills/**` should use managed sections, not full-file generation.
- 2026-04-30: `CLAUDE.md` should be preview-only in Q05 v0. Final root `CLAUDE.md` is deferred unless reviewed during Q05.
- 2026-04-30: `.claude/settings.json` is deferred in Q05 v0 to avoid unsafe hooks or auto-execution.
- 2026-04-30: `.claude/agents/**` may have preview-only role-limited definitions, but final `.claude/**` emission is deferred.
- 2026-04-30: Timestamps should be avoided in generated files; fingerprints are preferred.

## Validation And Acceptance

This plan-only task is acceptable when:

- `.aide/queue/Q05-generated-artifacts-v0/task.yaml` exists.
- `.aide/queue/Q05-generated-artifacts-v0/ExecPlan.md` exists and contains all required sections.
- `.aide/queue/Q05-generated-artifacts-v0/prompt.md` exists.
- `.aide/queue/Q05-generated-artifacts-v0/status.yaml` exists.
- `.aide/queue/Q05-generated-artifacts-v0/evidence/planning-validation.md` exists.
- `.aide/queue/index.yaml` references Q05 task, ExecPlan, prompt, and evidence paths.
- `PLANS.md` contains only a minimal Q05 planning pointer if updated.
- No implementation work, final generated artifacts, Harness implementation changes, final agent-surface changes, Q06+ work, or forbidden paths are modified.

Q05 implementation will be acceptable only when:

- Harness validation passes before generation or fails with actionable blockers.
- The bounded Q03-era Harness wording refresh is complete and validated before generation.
- Generated markers and manifest records are deterministic.
- Managed sections preserve manual content outside markers.
- Preview/final target choices match this target policy.
- `aide validate` detects stale, missing, markerless, or manually edited generated artifacts.
- Evidence records changed files, validation, generated artifact policy, and remaining risks.
- Q05 status moves to `needs_review` or `blocked` honestly.

## Idempotence And Recovery

A stateless worker can restart Q05 by reading:

- `AGENTS.md`
- `.aide/queue/policy.yaml`
- `.aide/queue/index.yaml`
- Q04 review evidence and Q04 status
- foundation review and full audit records
- Q00 through Q04 task packets and evidence
- Q03 contract files under `.aide/**`
- Q04 Harness files under `core/harness/**` and `scripts/aide`
- `docs/reference/source-of-truth.md`
- `docs/reference/harness-v0.md`
- this Q05 `task.yaml`, `ExecPlan.md`, `prompt.md`, and `status.yaml`

If partial Q05 implementation already exists, inspect `git status`, generated markers, `.aide/generated/manifest.yaml`, Q05 evidence, and Harness validation output before editing. Preserve unrelated user changes. If an unmarked final generated artifact appears, stop and record a blocker unless Q05 evidence explains it. If a managed section has manual edits inside markers, stop or preserve by moving changes outside the section only with explicit evidence.

## Evidence To Produce

Q05 implementation should produce:

- `.aide/queue/Q05-generated-artifacts-v0/evidence/changed-files.md`
- `.aide/queue/Q05-generated-artifacts-v0/evidence/validation.md`
- `.aide/queue/Q05-generated-artifacts-v0/evidence/generated-artifact-policy.md`
- `.aide/queue/Q05-generated-artifacts-v0/evidence/remaining-risks.md`
- `.aide/queue/Q05-generated-artifacts-v0/evidence/blocker.md` if blocked

The plan-only task produces:

- `.aide/queue/Q05-generated-artifacts-v0/evidence/planning-validation.md`

## Outcomes And Retrospective

Plan-only outcome:

- Q05 is planned and ready for a future implementation worker.
- Q05 implementation remains pending and review-gated.
- No generated artifacts were created.
- No final agent-facing outputs were modified.
- No Q06+ work was implemented.
