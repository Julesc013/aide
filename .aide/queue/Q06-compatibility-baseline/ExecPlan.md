# Q06 ExecPlan: Compatibility Baseline

## Purpose

Q06 will implement the first real AIDE Compatibility baseline. The baseline must make version, migration, replay, upgrade-gate, and deprecation posture enforceable enough for future queue work without building a full migration platform.

Q06 is still small by design. It governs how the AIDE Profile/Contract, queue records, Harness command metadata, generated artifact metadata, and compatibility records evolve. It does not implement Runtime, Hosts, Dominium Bridge behavior, provider/model calls, app surfaces, release automation, or autonomous service logic.

## Background And Current Repo Context

AIDE is being rebooted in place. Bootstrap-era implementation, docs, host proofs, matrices, research, environment, eval, packaging, and phase records remain preserved as evidence.

Current facts verified during Q06 planning:

- Q04 Harness v0 is implemented and passed review with `PASS_WITH_NOTES`.
- Q05 generated artifacts v0 is implemented and reviewed with `PASS_WITH_NOTES`.
- Q05 `status.yaml` and `.aide/queue/index.yaml` intentionally still say `needs_review` because the Q05 review avoided changing `.aide/queue/index.yaml`, which is part of the generated manifest source fingerprint.
- Q05 review evidence explicitly says Q06 planning may proceed.
- `py -3 scripts/aide validate`, `doctor`, `compile`, and `migrate` currently run and exit successfully with warnings only.
- Current Compatibility files are placeholders: `.aide/compat/schema-version.yaml`, `.aide/compat/migration-baseline.yaml`, and `core/compat/README.md`.
- `.aide/policies/generated-artifacts.yaml` still has Q03-era planned-boundary wording. Q05 review records this as a cleanup before Q07 or broader generation work, not a Q06 planning blocker.
- Q00 through Q03 remain `needs_review`; previous reviews and audits accepted proceeding with notes.

The future Q06 worker must re-verify these facts before implementation.

## Scope

Q06 implementation should:

- document the compatibility baseline in `docs/reference/compatibility-baseline.md`;
- define the v0 compatibility unit and supported version registry;
- add a small compatibility module or data-only equivalent under `core/compat/**`;
- add or update `.aide/compat/**` records for schema versions, migration baseline, replay corpus, upgrade gates, and deprecations;
- update `aide migrate` to report compatibility baseline details without mutating files;
- update `aide validate` to check known compatibility metadata and versions;
- add lightweight standard-library tests for compatibility helpers and command smoke;
- update only the minimal docs/root indexes needed to make Q06 visible;
- write Q06 evidence and stop at review.

## Non-goals

- Do not build a full migration engine.
- Do not apply or mutate migrations.
- Do not redefine product semantics or host support claims.
- Do not normalize all bootstrap-era inventory, matrix, or research records.
- Do not implement Runtime, Service, Hosts, Commander, Mobile, IDE extensions, Dominium Bridge, provider adapters, browser bridges, app surfaces, model calls, web search integrations, packaging, release automation, or autonomous service logic.
- Do not alter generated artifact behavior. If Q06 changes a Q05 manifest source input and the manifest becomes stale, use only existing Q05 generation behavior if the implementation prompt permits a refresh; otherwise record the expected warning.
- Do not create final `CLAUDE.md` or `.claude/**`.
- Do not implement Q07 or Q08.
- Do not delete or move bootstrap-era records.

## Allowed Paths For Q06 Implementation

- `core/compat/**`
- `core/harness/**` only for migrate/validate compatibility checks
- `core/contract/**` only if needed for version metadata or docs
- `.aide/compat/**`
- `.aide/toolchain.lock` only for compatibility version alignment
- `.aide/generated/**` only to record/check the Q05 generated manifest version or refresh existing Q05 outputs if Q06 source-input edits make refresh unavoidable and evidence-backed
- `.aide/commands/**` only if needed to update migrate/validate compatibility status metadata
- `.aide/evals/**` only if needed for compatibility/replay declarations
- `docs/reference/compatibility-baseline.md`
- `docs/reference/profile-contract-v0.md`
- `docs/reference/harness-v0.md`
- `docs/reference/generated-artifacts-v0.md`
- `docs/reference/source-of-truth.md`
- `README.md`
- `DOCUMENTATION.md`
- `ROADMAP.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `.aide/queue/Q06-compatibility-baseline/**`
- `.aide/queue/index.yaml`

## Forbidden Paths For Q06 Implementation

- `shared/**`
- existing `hosts/**` implementation/proof files
- `bridges/**`
- `core/runtime/**`
- `core/control/**` except conceptual docs references if needed
- `core/sdk/**`
- `governance/**`
- `inventory/**`
- `matrices/**`
- `research/**`
- `specs/**`
- `environments/**`
- `labs/**`
- `evals/**` except specifically allowed AIDE compatibility/replay declarations under `.aide/evals/**`
- `packaging/**`
- `.aide/policies/**` unless a future prompt explicitly expands scope for generated-artifact policy cleanup
- provider/model integrations
- web search integrations
- local model integrations
- runtime/broker/service code
- IDE/app/host code
- release/package automation
- Q07/Q08 implementation

## Compatibility Scope

Q06 compatibility covers repository evolution for:

- Profile/Contract schema and contract version records.
- Toolchain lock shape and compatibility posture.
- Queue policy and queue index schema identifiers.
- Harness command surface version and command availability posture.
- Generated artifact manifest version and generator version metadata.
- Compatibility policy, migration baseline, replay corpus, upgrade gates, and deprecation records.

Q06 compatibility does not cover:

- product feature semantics;
- host adapter behavior;
- Runtime, service, worker, or provider protocols;
- Dominium Bridge implementation;
- support/capability claim expansion beyond existing bootstrap policies;
- release or packaging artifacts.

## Version Model

Decision: Q06 uses explicit AIDE string identifiers, not dates and not semver.

Baseline identifiers should look like:

- `aide.profile-contract.v0`
- `aide.profile.v0`
- `aide.toolchain-lock.v0`
- `aide.queue-index.v0`
- `aide.queue-policy.v0`
- `aide.commands-catalog.v0`
- `aide.compat-schema-version.v0`
- `aide.migration-baseline.v0`
- `aide.generated-manifest.v0`
- `q05.generated-artifacts.v0`
- `aide.harness-command-surface.v0`
- `aide.compat-baseline.v0`

Rationale:

- The repo already uses string identifiers.
- String ids are readable and stable in Markdown/YAML.
- The current repo is pre-product and does not need semver promises.
- Dated versions would imply a calendar cadence that the queue does not use.

Q06 should record a version registry that maps each known surface to:

- id;
- current version;
- owner queue item;
- status;
- source path;
- compatibility posture;
- validation behavior for missing, current, deprecated, or unknown versions.

## Migration Model

Q06 migration is registry-first and no-op-safe.

Implementation should create a migration registry that includes:

- a current baseline entry such as `baseline-current-noop`;
- source version: `none` or `aide.profile-contract.v0`;
- target version: current baseline versions;
- status: `current-noop`;
- mutates_repo: `false`;
- owner queue item: `Q06-compatibility-baseline`;
- review requirement for any future mutating migration.

`aide migrate` after Q06 should:

- read `.aide/compat/**` records;
- report current known versions;
- report available migrations;
- report no-op when all current versions are known;
- warn or fail on unknown future versions according to the upgrade gate model;
- never mutate files in Q06.

No real migration from one schema to another should be implemented in Q06.

## Replay Baseline Model

Q06 replay means cheap deterministic compatibility replay, not Runtime replay.

The replay baseline should contain:

- a fixture or manifest listing current compatibility records;
- expected command summaries for `aide validate`, `aide doctor`, `aide compile --dry-run`, and `aide migrate`;
- expected zero hard errors on the current repo;
- expected warnings for accepted review-gated legacy statuses if still present;
- expected generated manifest/version checks if Q05 records exist.

Suggested locations:

- `.aide/compat/replay-corpus.yaml`
- `core/compat/replay_manifest.py` or a small data-only equivalent
- `core/compat/tests/**`

The replay corpus should use stable text anchors and summary expectations, not brittle full stdout snapshots.

## Upgrade Gate Model

Q06 should define a small machine-readable gate model in `.aide/compat/upgrade-gates.yaml`.

Initial gates:

- `allow_current`: known current version passes.
- `warn_deprecated`: known deprecated version warns with replacement guidance.
- `block_unknown_future`: unknown version greater/newer than current or unrecognized id is an error or blocker.
- `review_required_for_schema_change`: any schema id change needs a queue item and evidence.
- `review_required_for_generated_artifact_contract_change`: generated manifest/generator contract changes need review and drift evidence.
- `no_automatic_mutation`: migrations do not apply automatically in Q06.

Harness validation should use these gates conservatively. If exact future-version ordering cannot be determined from string ids, unknown ids should be treated as unsafe and actionable.

## Deprecation Model

Q06 should create `.aide/compat/deprecations.yaml` even if it has no active deprecations.

Each future deprecation record should include:

- deprecated id;
- deprecated version;
- replacement id/version if any;
- status: candidate, deprecated, blocked, removed, or superseded;
- owner queue item;
- review requirement;
- removal gate;
- evidence path.

Q06 should not remove any current v0 surface.

## Harness Migrate/Validate Changes

`aide migrate` should become the primary user-facing compatibility report:

- print compatibility baseline version;
- print current known surface versions;
- print no-op migration status;
- list future migration registry entries if any;
- report unknown future versions clearly;
- state that no files are mutated.

`aide validate` should check:

- required compatibility records exist;
- known v0 surface versions are present;
- `.aide/toolchain.lock` aligns with `.aide/compat/schema-versions.yaml`;
- queue index and policy schema versions are recognized;
- generated artifact manifest schema and generator version are recognized if `.aide/generated/manifest.yaml` exists;
- Harness command surface version metadata is present;
- deprecation and upgrade-gate records are structurally present.

Validation must remain honest: structural checks only unless Q06 deliberately adds small standard-library parsers.

## Planned Deliverables

Q06 implementation should create or update:

- `docs/reference/compatibility-baseline.md`
- `core/compat/README.md`
- `core/compat/version_registry.py` or a data-only equivalent
- `core/compat/migration_registry.py` or a data-only equivalent
- `core/compat/replay_manifest.py` or a data-only equivalent
- `core/compat/tests/**`
- `.aide/compat/schema-versions.yaml`
- `.aide/compat/migration-baseline.yaml`
- `.aide/compat/replay-corpus.yaml`
- `.aide/compat/upgrade-gates.yaml`
- `.aide/compat/deprecations.yaml`
- `.aide/toolchain.lock` with narrowly scoped compatibility version alignment if needed
- `.aide/commands/catalog.yaml` only if command metadata needs to describe Q06 migrate/validate behavior
- `.aide/evals/catalog.yaml` only if compatibility/replay eval declarations need Q06 status updates
- Harness migrate/validate compatibility checks under `core/harness/**`
- docs references in `profile-contract-v0.md`, `harness-v0.md`, `generated-artifacts-v0.md`, `source-of-truth.md`, `DOCUMENTATION.md`, `README.md`, `ROADMAP.md`, `PLANS.md`, and `IMPLEMENT.md` only where needed
- Q06 evidence under `.aide/queue/Q06-compatibility-baseline/evidence/**`

If Q06 edits any file that is a Q05 generated-artifact source input, the worker must run `py -3 scripts/aide validate` and record whether the generated manifest became stale. If the Q06 prompt permits refreshing Q05 outputs, use only existing `aide compile --write`; do not change generated artifact behavior.

## Milestones

1. Re-read AGENTS, queue policy, Q04/Q05 reviews, Q03-Q05 outputs, Q06 task packet, contract records, Harness files, generated-artifact docs, current compatibility skeleton, and root docs.
2. Confirm Q04 is `passed` and Q05 review evidence records `PASS_WITH_NOTES`.
3. Run baseline `py -3 scripts/aide validate`, `doctor`, `compile`, and `migrate`.
4. Update Q06 status to `running` only after confirming allowed paths.
5. Define compatibility baseline docs and `.aide/compat/**` records.
6. Add small `core/compat/**` helpers or data-only records.
7. Update Harness migrate/validate compatibility checks without adding external dependencies.
8. Add lightweight tests and replay baseline checks.
9. Update root/reference docs minimally.
10. Run validation, migrate, compile dry-run, tests, queue helpers, diff check, and allowed-path audit.
11. Write Q06 evidence.
12. Stop at `needs_review` or write blocker evidence if blocked.

## Progress

- 2026-04-30: Q06 plan-only packet created after Q05 review commit `2385156 Review Q05 generated artifacts v0`.
- 2026-04-30: Q06 planning accepted Q05 `PASS_WITH_NOTES` review evidence as the dependency gate, while preserving the fact that Q05 queue status remains `needs_review` to avoid generated manifest drift.
- 2026-04-30: Q06 planning chose AIDE string version identifiers, a no-op migration registry, a small replay baseline, and conservative upgrade/deprecation records.
- 2026-04-30: No Q06 implementation, final compatibility records, Harness changes, generated artifact behavior changes, Dominium Bridge behavior, Runtime, Hosts, or Q07+ work were created by this plan-only task.
- 2026-04-30: Q06 implementation added `.aide/compat/**` v0 records for schema versions, no-op migration baseline, replay corpus, upgrade gates, and deprecations.
- 2026-04-30: Q06 implementation added `core/compat/**` standard-library helpers and tests for the version registry, migration registry, and replay expectations.
- 2026-04-30: Harness `validate` now checks compatibility records and known versions; Harness `migrate` now reports the Q06 compatibility baseline and `baseline-current-noop` migration entry without mutating files.
- 2026-04-30: Reference and root docs were updated to describe the Q06 baseline and its non-goals.
- 2026-04-30: Existing Q05 `aide compile --write` was used only to refresh `.aide/generated/manifest.yaml` after Q06 changed approved source inputs; no generated behavior or target policy was changed.
- 2026-04-30: Q06 status moved to `needs_review` after validation and evidence were prepared.

## Surprises And Discoveries

- Q05 review intentionally left `.aide/queue/index.yaml` and Q05 `status.yaml` unchanged because `.aide/queue/index.yaml` is part of the Q05 generated manifest source fingerprint. Q06 planning must document this rather than treating raw Q05 status as failure.
- Updating `.aide/queue/index.yaml` for Q06 planning can make the Q05 manifest source fingerprint stale. This is expected because Q06 planning is not allowed to refresh generated artifacts.
- `.aide/policies/generated-artifacts.yaml` still says generated artifacts are planned, but Q05 review records this as a cleanup before Q07 or broader generation work, not a Q06 planning blocker.
- Q06 implementation could not update `.aide/profile.yaml` current-focus wording because it is not in the Q06 allowlist. Compatibility truth for Q06 therefore lives in `.aide/compat/**`, `.aide/toolchain.lock`, docs, and queue evidence.
- Generated sections in `AGENTS.md` and `.agents/skills/**` still contain Q05-era concise wording because Q06 does not change generated artifact behavior or managed target bodies.

## Decision Log

- 2026-04-30: Q06 planning may proceed based on Q05 review outcome `PASS_WITH_NOTES` even though raw Q05 queue status remains `needs_review`.
- 2026-04-30: The v0 compatibility unit is the set of repo evolution surfaces: Profile/Contract, toolchain lock, queue policy/index, Harness command surface, generated manifest/generator metadata, and compatibility records.
- 2026-04-30: Q06 uses AIDE string version identifiers such as `aide.profile.v0`; it does not introduce semver or dated versions.
- 2026-04-30: Q06 implements a no-op current migration registry only; no real migrations and no apply mode.
- 2026-04-30: Replay baseline means deterministic Harness/compatibility summary replay, not Runtime replay.
- 2026-04-30: Unknown future versions should be reported as unsafe and actionable.
- 2026-04-30: Deprecation records should exist even if there are no active deprecations.
- 2026-04-30: Preserve `.aide/compat/schema-version.yaml` as a Q03-era singular compatibility record for existing v0 readers, and add `.aide/compat/schema-versions.yaml` as the Q06 registry.
- 2026-04-30: Keep `aide migrate` non-mutating; no apply flag or migration engine is introduced.
- 2026-04-30: Treat replay as stable Harness summary expectations instead of full stdout snapshots or Runtime replay.

## Validation And Acceptance

This plan-only task is acceptable when:

- `.aide/queue/Q06-compatibility-baseline/task.yaml` exists.
- `.aide/queue/Q06-compatibility-baseline/ExecPlan.md` exists and contains all required sections.
- `.aide/queue/Q06-compatibility-baseline/prompt.md` exists.
- `.aide/queue/Q06-compatibility-baseline/status.yaml` exists.
- `.aide/queue/Q06-compatibility-baseline/evidence/planning-validation.md` exists.
- `.aide/queue/index.yaml` references Q06 task, ExecPlan, prompt, and evidence paths.
- Q04 passed status is confirmed.
- Q05 accepted-equivalent review evidence is confirmed.
- Validation commands are recorded.
- No implementation work or forbidden paths are modified.

Q06 implementation will be acceptable only when:

- compatibility docs and records define supported v0 versions;
- migration registry exists and is no-op-safe;
- replay corpus baseline exists and is cheap/deterministic;
- upgrade gates and deprecation records exist;
- Harness `validate` and `migrate` report compatibility posture honestly;
- unknown future versions are handled safely;
- Q06 evidence is complete;
- Q06 stops at review.

## Idempotence And Recovery

A stateless worker can restart Q06 by reading:

- `AGENTS.md`
- `.aide/queue/policy.yaml`
- `.aide/queue/index.yaml`
- Q04 review evidence
- Q05 implementation and review evidence
- Q03 contract records under `.aide/**`
- Q04/Q05 Harness files under `core/harness/**` and `scripts/aide`
- Q05 generated manifest and generated-artifact docs
- current `core/compat/**`, `.aide/compat/**`, and `docs/charters/compatibility-charter.md`
- this Q06 `task.yaml`, `ExecPlan.md`, `prompt.md`, and `status.yaml`

If partial Q06 implementation exists, run `py -3 scripts/aide validate`, inspect `.aide/compat/**`, inspect `core/compat/**`, and review Q06 evidence before editing. Preserve unrelated user changes. If compatibility changes would require broader contract rewriting or generated behavior changes, stop and write blocker evidence.

## Evidence To Produce

Q06 implementation should produce:

- `.aide/queue/Q06-compatibility-baseline/evidence/changed-files.md`
- `.aide/queue/Q06-compatibility-baseline/evidence/validation.md`
- `.aide/queue/Q06-compatibility-baseline/evidence/compatibility-policy.md`
- `.aide/queue/Q06-compatibility-baseline/evidence/replay-baseline.md`
- `.aide/queue/Q06-compatibility-baseline/evidence/remaining-risks.md`
- `.aide/queue/Q06-compatibility-baseline/evidence/blocker.md` if blocked

The plan-only task produces:

- `.aide/queue/Q06-compatibility-baseline/evidence/planning-validation.md`

## Outcomes And Retrospective

Plan-only outcome:

- Q06 is planned and ready for a future implementation worker.
- Q06 implementation remains pending and review-gated.
- No final compatibility baseline, migration engine, Harness compatibility code, or generated artifact behavior changes were implemented.
- Q07 Dominium Bridge baseline, Runtime, Hosts, provider adapters, app surfaces, release automation, and autonomous service logic remain deferred.

Implementation outcome:

- Q06 Compatibility baseline v0 is implemented and stopped at `needs_review`.
- The baseline records known v0 versions, one no-op current migration, structural replay expectations, upgrade gates, and deprecation format.
- Harness `validate` and `migrate` report the baseline using standard-library structural checks.
- No real migrations, migration apply mode, Dominium Bridge implementation, Runtime, Hosts, providers, generated artifact behavior changes, app surfaces, release automation, or Q07+ work were added.
