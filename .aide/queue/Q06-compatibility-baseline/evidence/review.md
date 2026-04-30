# Q06 Compatibility Baseline Review

Date: 2026-04-30
Reviewer: GPT-5.5 Codex
Reviewed commit: `5327e59 Implement Q06 compatibility baseline`

## Executive Verdict

Q06 satisfies its ExecPlan well enough to accept the Compatibility baseline and proceed to Q07 Dominium Bridge baseline planning.

Final review outcome: `PASS_WITH_NOTES`

The implementation makes Compatibility first-class through `.aide/compat/**` records, `core/compat/**` standard-library helpers, Harness `validate` and `migrate` checks, and reference documentation. It remains conservative: migrations are current-baseline/no-op only, replay is structural Harness summary replay rather than Runtime replay, unknown future versions are treated as unsafe, and no product/runtime/host/provider/Dominium behavior was added.

## Scope Review

Q06 stayed inside the planned Compatibility baseline scope. The changed-file evidence lists only allowed Q06 paths: `.aide/compat/**`, `core/compat/**`, narrow Harness validate/migrate changes, compatibility/toolchain/command/eval metadata, the Q05 generated manifest refresh caused by approved source-input edits, reference/root docs, queue metadata, and Q06 evidence.

No forbidden Runtime, Host, Bridge, Commander, Mobile, IDE extension, provider, browser, app, release, packaging, or Q07+ implementation was found.

## Compatibility Model Review

Compatibility is now represented as an explicit repo-evolution domain. The implemented baseline covers Profile/Contract versions, toolchain lock posture, queue schema versions, Harness command surface version, generated manifest/generator versions, compatibility records, migration posture, replay metadata, upgrade gates, and deprecation records.

The model does not redefine downstream product semantics. Docs and records repeatedly state that Compatibility governs evolution metadata, not Runtime, Host, Bridge, provider, or release behavior.

## Version Model Review

Q06 chose AIDE string identifiers, matching the ExecPlan. The canonical registry is `.aide/compat/schema-versions.yaml`, mirrored by `core/compat/version_registry.py`.

Review confirmed current known versions for:

- `aide.profile-contract.v0`
- `aide.profile.v0`
- `aide.toolchain-lock.v0`
- `aide.queue-index.v0`
- `aide.queue-policy.v0`
- `aide.queue-status.v0`
- `aide.commands-catalog.v0`
- `aide.compat-baseline.v0`
- `aide.compat-schema-versions.v0`
- `aide.migration-baseline.v0`
- `aide.replay-corpus.v0`
- `aide.upgrade-gates.v0`
- `aide.deprecations.v0`
- `aide.generated-manifest.v0`
- `q05.generated-artifacts.v0`
- `aide.harness-command-surface.v0`

`classify_version("profile", "aide.profile.v99")` is covered by tests and returns an error posture for unknown/future versions.

## Migration Model Review

The migration model is appropriately narrow. `.aide/compat/migration-baseline.yaml` and `core/compat/migration_registry.py` define one entry, `baseline-current-noop`, with `mutates_repo: false`.

`py -3 scripts/aide migrate` reports:

- `compatibility_baseline_version: aide.compat-baseline.v0`
- `mutation: none`
- `migration_engine: no-op-current-baseline`
- `automatic_migrations: none`
- `mutating_migrations_available: false`
- `unknown_future_versions: error`
- `migration_needed: false`

No migration apply mode or destructive migration behavior was found.

## Replay Baseline Review

The replay baseline exists at `.aide/compat/replay-corpus.yaml` and `core/compat/replay_manifest.py`. It covers deterministic Harness summary expectations for validate, doctor, compile dry-run, and migrate.

The record explicitly declares `runtime_replay: false`, avoids provider/model/native/browser/network calls, and uses summary anchors rather than brittle full stdout snapshots. This matches the Q06 boundary.

## Upgrade Gate Review

`.aide/compat/upgrade-gates.yaml` defines the expected v0 gate ids:

- `allow_current`
- `warn_deprecated`
- `block_unknown_future`
- `review_required_for_schema_change`
- `review_required_for_generated_artifact_contract_change`
- `no_automatic_mutation`

Harness validation reports the gate record as present. The gate model is conservative enough for Q07 planning.

## Deprecation Model Review

`.aide/compat/deprecations.yaml` exists, defines the record format, and keeps `active_deprecations: []`.

No current v0 surface is deprecated by Q06, which is the correct conservative posture.

## Harness Migrate And Validate Behavior Review

`aide validate` now checks required compatibility records and known v0 versions. It reports compatibility version findings, upgrade gates, deprecation format, replay posture, generated manifest version, and generated artifact generator version.

`aide migrate` is a Compatibility baseline report, not a migration engine. It reads the registry, reports current versions and the no-op migration entry, and exits successfully when the current repo has no compatibility errors.

Both commands are structural and standard-library based. They do not claim full YAML or JSON Schema validation.

## Source-Of-Truth Review

The source-of-truth boundaries remain coherent:

- `.aide/` remains canonical for Profile/Contract and compatibility records.
- `.aide/queue/` remains canonical for queue execution state.
- `.aide/generated/**` remains generated or preview output, not canonical truth.
- bootstrap-era records remain historical evidence and inputs.

Notes remain for follow-up freshness: `.aide/profile.yaml` still contains Q05-era current-focus wording and says `compatibility_baseline: not_implemented`; `.aide/policies/generated-artifacts.yaml` still has Q03-era planned-boundary wording; generated summaries in `AGENTS.md` and `.agents/skills/**` still have Q05-era concise deferrals. These are real cleanup items, but they do not make Q07 planning unsafe because `.aide/compat/**`, `.aide/toolchain.lock`, docs, Harness output, and Q06 evidence now identify the implemented Q06 baseline.

## No-Scope-Creep Review

Scope scans found no external dependency, provider/model/network/browser integration, Runtime/Service/Broker code, Host/App/Extension implementation, Dominium Bridge implementation, release automation, or destructive migration apply behavior.

The only `subprocess` use found is in Harness tests for local command smoke checks.

## Evidence Completeness Review

Required Q06 implementation evidence exists:

- `.aide/queue/Q06-compatibility-baseline/evidence/changed-files.md`
- `.aide/queue/Q06-compatibility-baseline/evidence/validation.md`
- `.aide/queue/Q06-compatibility-baseline/evidence/compatibility-policy.md`
- `.aide/queue/Q06-compatibility-baseline/evidence/replay-baseline.md`
- `.aide/queue/Q06-compatibility-baseline/evidence/remaining-risks.md`

This review adds:

- `.aide/queue/Q06-compatibility-baseline/evidence/review.md`
- `.aide/queue/Q06-compatibility-baseline/evidence/review-validation.md`
- `.aide/queue/Q06-compatibility-baseline/evidence/review-risks.md`
- `.aide/queue/Q06-compatibility-baseline/evidence/review-recommendation.md`

## Q07 Readiness Implication

Q07 planning may proceed. Q07 must treat Q06 as a compatibility foundation, not as permission to implement Runtime, broad Bridges, provider adapters, hosts, generated targets, or service logic.

Q07 planning should read this review evidence and account for the remaining cleanup notes before relying on high-level generated summaries.

## Status Update Decision

This review intentionally leaves Q06 `status.yaml` and `.aide/queue/index.yaml` unchanged. `.aide/queue/index.yaml` is a Q05 generated-manifest source input, and this review task is forbidden from refreshing generated artifacts. Updating index status during review would create hidden generated-manifest drift.

The review outcome is recorded in evidence as `PASS_WITH_NOTES`; Q07 planning may proceed from this record.

## Final Review Outcome

`PASS_WITH_NOTES`
