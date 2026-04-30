# Core Compatibility

## Purpose

Compatibility keeps AIDE repo evolution tied to explicit version, migration, replay, upgrade-gate, and deprecation records.

Q06 implements the first enforceable Compatibility baseline for the self-hosting repo. The baseline covers the Profile/Contract, toolchain lock, queue schemas, Harness command surface, generated artifact manifest/generator metadata, and compatibility records.

## Implemented Baseline

The Q06 baseline is intentionally small:

- `version_registry.py` lists known v0 surfaces and their current AIDE string identifiers.
- `migration_registry.py` exposes one current no-op migration entry, `baseline-current-noop`.
- `replay_manifest.py` records cheap Harness summary expectations, not Runtime replay.
- `tests/**` verifies the registry, no-op migration posture, replay metadata, and current repo records.

All code uses the Python standard library. No external YAML parser, migration engine, provider integration, Runtime behavior, Host behavior, Dominium Bridge implementation, or release automation is introduced here.

## Records

The canonical compatibility records live under `.aide/compat/**`:

- `schema-versions.yaml`
- `migration-baseline.yaml`
- `replay-corpus.yaml`
- `upgrade-gates.yaml`
- `deprecations.yaml`

The older singular `schema-version.yaml` is preserved for existing v0 readers and points to the Q06 registry.

## Boundaries

Compatibility governs evolution of AIDE repo contracts and generated/Harness metadata. It does not define downstream product semantics.

Existing `inventory/**`, `matrices/**`, `research/**`, `environments/**`, `evals/**`, and host proof records remain in place as bootstrap-era evidence.
