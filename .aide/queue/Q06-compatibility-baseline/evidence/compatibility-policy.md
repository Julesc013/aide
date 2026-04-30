# Q06 Compatibility Policy Evidence

Date: 2026-04-30

## Baseline Version Model

Q06 uses AIDE string identifiers, not semver or dated versions.

Primary ids:

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

The canonical Q06 registry is `.aide/compat/schema-versions.yaml`. `core/compat/version_registry.py` mirrors this registry for Harness structural checks.

## Migration Model

Q06 implements one current no-op migration entry:

- `baseline-current-noop`

Properties:

- source version: `none`
- target version: `aide.compat-baseline.v0`
- status: `current-noop`
- `mutates_repo: false`
- no apply mode

`aide migrate` reports this registry and never mutates files in Q06.

## Upgrade Gates

Implemented gates:

- `allow_current`
- `warn_deprecated`
- `block_unknown_future`
- `review_required_for_schema_change`
- `review_required_for_generated_artifact_contract_change`
- `no_automatic_mutation`

Unknown or future version ids are treated as errors rather than accepted silently.

## Deprecations

`.aide/compat/deprecations.yaml` defines a deprecation record format and sets:

```yaml
active_deprecations: []
```

No current v0 compatibility surface is deprecated by Q06.

## Boundaries

Compatibility governs repo evolution surfaces. It does not define product semantics, Runtime behavior, Host behavior, provider behavior, Dominium Bridge behavior, packaging, release automation, or autonomous service execution.
