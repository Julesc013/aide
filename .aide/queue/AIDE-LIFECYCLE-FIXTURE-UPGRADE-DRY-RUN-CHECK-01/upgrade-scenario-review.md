# Upgrade Scenario Review

| Scenario | Expected status | Expected blocker | Expected report | Result |
| --- | --- | --- | --- | --- |
| `upgrade-v2` | `PASS_WITH_WARNINGS` | none | present | PASS |
| `upgrade-manual-preserved` | `PASS_WITH_WARNINGS` | none | absent | PASS_WITH_WARNINGS |
| `drift-detected` | `BLOCKED` | `BLOCKED_DRIFT_DETECTED` | present | PASS |

All scenarios preserve path boundaries, managed-section expectations, hash references, no-apply fields, and review-gated capability labels.
