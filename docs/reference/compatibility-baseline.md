# Compatibility Baseline

## Purpose

The Q06 Compatibility baseline makes AIDE repo evolution explicit and reviewable. It records known v0 versions, no-op migration posture, replay expectations, upgrade gates, and deprecation rules for the self-hosting Profile/Contract, Harness, queue, generated artifacts, and compatibility records.

Compatibility is an AIDE Core domain. It governs how repo contract surfaces evolve; it does not define product behavior, Runtime semantics, Host implementations, Bridges, providers, browser integrations, release automation, or app surfaces.

## Scope

Q06 compatibility covers:

- `.aide/profile.yaml` and Profile/Contract v0 identifiers;
- `.aide/toolchain.lock` compatibility alignment;
- `.aide/queue/policy.yaml`, `.aide/queue/index.yaml`, and queue status record identifiers;
- `.aide/commands/catalog.yaml` Harness command-surface posture;
- `.aide/generated/manifest.yaml` schema and generator identifiers from Q05;
- `.aide/compat/**` version, migration, replay, upgrade-gate, and deprecation records;
- Harness `validate` and `migrate` structural checks for those records.

Q06 does not cover:

- Runtime, broker, scheduler, router, worker, or service behavior;
- AIDE Hosts, Commander, Mobile, IDE/editor extensions, or app surfaces;
- Dominium Bridge or XStack implementation;
- provider, model, browser, network, or web search integrations;
- packaging, release, signing, or install automation;
- product feature semantics.

## Version Vocabulary

Q06 uses explicit AIDE string identifiers. It does not introduce semver or dated versions.

Supported v0 identifiers include:

| Surface | Current version |
| --- | --- |
| Profile/Contract | `aide.profile-contract.v0` |
| Profile file | `aide.profile.v0` |
| Toolchain lock | `aide.toolchain-lock.v0` |
| Queue index | `aide.queue-index.v0` |
| Queue policy | `aide.queue-policy.v0` |
| Queue status | `aide.queue-status.v0` |
| Commands catalog | `aide.commands-catalog.v0` |
| Compatibility baseline | `aide.compat-baseline.v0` |
| Compatibility schema versions | `aide.compat-schema-versions.v0` |
| Migration baseline | `aide.migration-baseline.v0` |
| Replay corpus | `aide.replay-corpus.v0` |
| Upgrade gates | `aide.upgrade-gates.v0` |
| Deprecations | `aide.deprecations.v0` |
| Generated manifest | `aide.generated-manifest.v0` |
| Generated artifact generator | `q05.generated-artifacts.v0` |
| Harness command surface | `aide.harness-command-surface.v0` |

The canonical registry is `.aide/compat/schema-versions.yaml`. `core/compat/version_registry.py` mirrors the supported v0 surfaces for Harness checks.

Unknown or future version ids are not silently accepted. Q06 treats them as hard compatibility errors until a reviewed queue item updates the registry.

## Migration Registry

Q06 creates a migration registry with one current entry:

- `baseline-current-noop`

That entry records the current baseline only. It has:

- source version: `none`;
- target version: `aide.compat-baseline.v0`;
- status: `current-noop`;
- `mutates_repo: false`;
- no apply mode.

`aide migrate` reports the current version registry and available migration entries. It does not mutate files, apply migrations, rewrite contract records, or infer future migration behavior.

## Replay Corpus

Q06 replay means deterministic Harness summary expectations, not Runtime replay.

The replay record lives at `.aide/compat/replay-corpus.yaml` and covers:

- `py -3 scripts/aide validate`;
- `py -3 scripts/aide doctor`;
- `py -3 scripts/aide compile --dry-run`;
- `py -3 scripts/aide migrate`.

The replay baseline checks for zero hard errors on the current repo and accepts known review-gate warnings while Q00-Q03, Q05, or Q06 remain review-gated. It uses stable summary anchors rather than full stdout snapshots.

## Upgrade Gates

The gate record lives at `.aide/compat/upgrade-gates.yaml`.

Initial gate ids:

- `allow_current`
- `warn_deprecated`
- `block_unknown_future`
- `review_required_for_schema_change`
- `review_required_for_generated_artifact_contract_change`
- `no_automatic_mutation`

These gates are conservative. Q06 does not infer ordering for arbitrary future string ids; unrecognized ids require review.

## Deprecation Rules

The deprecation record lives at `.aide/compat/deprecations.yaml`.

Q06 defines the record format and keeps `active_deprecations: []`. No current v0 compatibility surface is deprecated by Q06.

Future deprecation records must name:

- deprecated id;
- deprecated version;
- replacement id/version if any;
- status;
- owner queue item;
- review requirement;
- removal gate;
- evidence path.

## Harness Behavior

`aide validate` checks that compatibility records exist and that known v0 versions are present. It reports missing or unknown versions as errors and current versions as info.

`aide migrate` reports:

- compatibility baseline version;
- current known surface versions;
- available no-op migration entries;
- no mutation;
- unknown future version behavior.

Both commands remain structural and standard-library only. They do not perform full YAML/schema validation.

Q08 `aide self-check` includes a Compatibility smoke summary. It reads the same known v0 surface registry and reports mutating migrations as unavailable. It does not add migration apply behavior or change Compatibility records.

## Non-Goals

Q06 does not build a full migration platform. It does not add real migrations, shims, Runtime replay, host compatibility automation, provider adapters, Dominium Bridge behavior, generated artifact regeneration behavior, release logic, or autonomous service execution.

## Implemented Now

Implemented by Q06:

- `.aide/compat/schema-versions.yaml`
- `.aide/compat/migration-baseline.yaml`
- `.aide/compat/replay-corpus.yaml`
- `.aide/compat/upgrade-gates.yaml`
- `.aide/compat/deprecations.yaml`
- `core/compat/version_registry.py`
- `core/compat/migration_registry.py`
- `core/compat/replay_manifest.py`
- lightweight compatibility tests
- Harness `validate` and `migrate` compatibility checks

Q06 stopped at review before Q07 Dominium Bridge work. Q07 now consumes this baseline through AIDE-side bridge pinning records without changing Q06 migration behavior.

## Dominium Bridge Pinning

Q07 adds AIDE-side Dominium Bridge compatibility and pinning records under `bridges/dominium/compatibility.yaml`.

Those records reference `aide.compat-baseline.v0` and the Q05 generated artifact identifiers. They do not create a separate compatibility version system and do not add mutating migrations.

Dominium adoption later should pin an AIDE commit, reviewed bundle, or future release artifact through a separate Dominium-side task. Q07 records the bridge pinning model only.
