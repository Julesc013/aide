# Determinism And Immutability

The helper validates deterministic repeated projection and reports:

- `deterministic_projection: true`
- `source_artifacts_mutated: false`

Focused tests also verify repeated byte-identical projection in a temporary
workspace and confirm accepted Interop Export source artifacts remain unchanged.

The build does not edit `.aide/interop/exports/**` or accepted Interop Export
build/check/accept reports.
