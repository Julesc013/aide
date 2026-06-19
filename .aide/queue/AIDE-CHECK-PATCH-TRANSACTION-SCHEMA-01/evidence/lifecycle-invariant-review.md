# Lifecycle Invariant Review Evidence

The deterministic example remains no later than `review_candidate`.

Confirmed invalid or unproducible combinations:

- `apply_performed: true` for this projection;
- `target_mutated: true` for this projection;
- `approval_granted: true` without accepted authority;
- `applied` with `apply_performed: false`;
- `rolled_back` with `rollback_performed: false`;
- ConformanceResult ref causing `trusted: true`.

No record claims approval, apply, target mutation, rollback execution, or trust.

Result: `PASS`
