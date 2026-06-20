# Determinism And Immutability

The helper's validation path performs a temp-workspace repeated-projection
comparison.

`a2a-agent-card-contract validate` reports:

- deterministic projection: `true`
- source artifacts mutated: `false`

Focused tests also compare repeated projection bytes and confirm accepted
predecessor reports and Interop Export artifacts remain unchanged.
