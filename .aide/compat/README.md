# AIDE Contract Compatibility

## Purpose

This directory records compatibility declarations for the AIDE self-hosting Profile/Contract, queue, Harness, generated artifact, migration, replay, upgrade-gate, and deprecation posture.

## Current Files

- `schema-versions.yaml`: Q06 canonical registry of known v0 compatibility surfaces and version ids.
- `schema-version.yaml`: preserved Q03-era singular schema-version record for existing v0 readers.
- `migration-baseline.yaml`: Q06 current no-op migration registry.
- `replay-corpus.yaml`: structural Harness summary replay baseline, not Runtime replay.
- `upgrade-gates.yaml`: conservative gates for current, deprecated, unknown future, schema-change, generated-artifact contract-change, and no-automatic-mutation behavior.
- `deprecations.yaml`: deprecation record format with no active deprecations in Q06.

## Boundary

Q06 does not implement a mutating migration engine, shims, Runtime replay, product semantics, Dominium Bridge behavior, provider integrations, host behavior, release automation, or autonomous service logic.
