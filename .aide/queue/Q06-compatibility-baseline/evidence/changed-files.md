# Q06 Changed Files

Date: 2026-04-30

## Compatibility Records

- `.aide/compat/schema-versions.yaml`
- `.aide/compat/schema-version.yaml`
- `.aide/compat/migration-baseline.yaml`
- `.aide/compat/replay-corpus.yaml`
- `.aide/compat/upgrade-gates.yaml`
- `.aide/compat/deprecations.yaml`
- `.aide/toolchain.lock`
- `.aide/commands/catalog.yaml`
- `.aide/evals/catalog.yaml`

## Compatibility Helpers

- `core/compat/README.md`
- `core/compat/__init__.py`
- `core/compat/version_registry.py`
- `core/compat/migration_registry.py`
- `core/compat/replay_manifest.py`
- `core/compat/tests/__init__.py`
- `core/compat/tests/test_compat_baseline.py`

## Harness

- `core/harness/README.md`
- `core/harness/commands.py`

## Generated Manifest

- `.aide/generated/manifest.yaml`

This was refreshed with the existing Q05 `py -3 scripts/aide compile --write` path because Q06 changed approved generated-artifact source inputs. No generated target policy or generator behavior was changed.

## Documentation

- `docs/reference/compatibility-baseline.md`
- `docs/reference/profile-contract-v0.md`
- `docs/reference/harness-v0.md`
- `docs/reference/generated-artifacts-v0.md`
- `docs/reference/source-of-truth.md`
- `README.md`
- `ROADMAP.md`
- `DOCUMENTATION.md`
- `PLANS.md`
- `IMPLEMENT.md`

## Queue And Evidence

- `.aide/queue/index.yaml`
- `.aide/queue/Q06-compatibility-baseline/ExecPlan.md`
- `.aide/queue/Q06-compatibility-baseline/status.yaml`
- `.aide/queue/Q06-compatibility-baseline/evidence/changed-files.md`
- `.aide/queue/Q06-compatibility-baseline/evidence/validation.md`
- `.aide/queue/Q06-compatibility-baseline/evidence/compatibility-policy.md`
- `.aide/queue/Q06-compatibility-baseline/evidence/replay-baseline.md`
- `.aide/queue/Q06-compatibility-baseline/evidence/remaining-risks.md`

## Explicit Non-Changes

- No real migration engine or apply mode was added.
- No Runtime, Service, Host, Commander, Mobile, IDE extension, provider, browser, app, release, packaging, or Dominium Bridge behavior was added.
- No final `CLAUDE.md` or `.claude/**` target was created.
- No `shared/**`, existing `hosts/**`, `bridges/**`, `core/runtime/**`, `core/control/**`, `core/sdk/**`, governance, inventory, matrices, research, specs, environments, labs, top-level `evals/**`, or packaging path was modified.
