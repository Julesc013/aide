# Profile Shape

## Purpose

`profile.yaml` identifies the repository and declares its current Contract/Profile posture.

## Required Fields

- `schema_version`
- `profile_contract_version`
- `profile_id`
- `profile_mode`
- `repo_identity`
- `lifecycle`
- `public_model`
- `internal_core_split`
- `first_shipped_stack`
- `implemented_reality`
- `future_intent`
- `rules`

## Status Rules

Use explicit states such as `implemented`, `partial`, `planned`, `deferred`, `not_implemented`, `skeleton_only`, and `implemented-bootstrap-era`.

## Boundary

The Profile is declarative. It must not define executable Harness behavior or claim Runtime, Hosts, Bridges, generated artifacts, or provider integrations are implemented.
