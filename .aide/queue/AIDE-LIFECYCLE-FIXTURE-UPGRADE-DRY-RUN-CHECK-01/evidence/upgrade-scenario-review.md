# Upgrade Scenario Review

Result: `PASS_WITH_WARNINGS`

| Scenario | Expected status | Expected blocker | Path | Managed section | Drift | Hash | Mutation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `upgrade-v2` | `PASS_WITH_WARNINGS` | none | PASS | PASS | not applicable | PASS | PASS |
| `upgrade-manual-preserved` | `PASS_WITH_WARNINGS` | none | PASS | PASS | not applicable | PASS | PASS |
| `drift-detected` | `BLOCKED` | `BLOCKED_DRIFT_DETECTED` | PASS | PASS | PASS | PASS | PASS |

`upgrade-manual-preserved` has no static expected report ref; this is non-blocking but repair-worthy.
