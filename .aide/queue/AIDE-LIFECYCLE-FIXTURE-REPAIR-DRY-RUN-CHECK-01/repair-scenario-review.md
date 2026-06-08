# Repair Scenario Review

Result: `PASS_WITH_WARNINGS`

| Scenario | Expected Status | Expected Blocker | Path | Marker | Hash | Mutation State | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `repair-plan-missing-marker` | `BLOCKED` | `BLOCKED_MARKER_MISSING` | PASS | PASS | PASS | PASS | Static expected repair report ref absent; expected-state README and generated plan report used as evidence. |
| `repair-plan-malformed-marker` | `BLOCKED` | `BLOCKED_MARKER_MALFORMED` | PASS | PASS | PASS | PASS | Static expected repair report ref absent; expected-state README and generated plan report used as evidence. |

The review confirms both generated repair plans use `mode=report`, fixture-only targets, explicit path `manual/with-managed-section.md`, blocked validation operations, expected preimage hashes, and no apply execution. The generated plan reports preserve the same expected statuses and blocker labels.
