# Toolchain Lock Shape

## Purpose

`toolchain.lock` records the minimal Contract/Profile v0 tooling posture.

## Required Fields

- `schema_version`
- `profile_contract_version`
- `profile_schema_version`
- `queue_index_schema_version`
- `queue_policy_version`
- `contract_tooling`
- `harness`
- `generated_artifacts`
- `package_or_install_automation`
- `limitations`

## Boundary

The lockfile must not claim package, worker, model, generated-artifact, runtime, service, or full toolchain automation that does not exist.
