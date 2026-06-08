# Repair Scenario Matrix

| Scenario | Check State | Expected Status | Expected Blocker | Plan | Expected Report Evidence | Path Boundary | Managed Section Marker | Hash | Mutation State | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| repair-plan-missing-marker | PASS_WITH_WARNINGS | BLOCKED | BLOCKED_MARKER_MISSING | PASS | PASS_WITH_WARNINGS | PASS | PASS | PASS | PASS | static expected repair report ref absent; expected-state README and generated plan report used |
| repair-plan-malformed-marker | PASS_WITH_WARNINGS | BLOCKED | BLOCKED_MARKER_MALFORMED | PASS | PASS_WITH_WARNINGS | PASS | PASS | PASS | PASS | static expected repair report ref absent; expected-state README and generated plan report used |

Residual risk for both scenarios: static report-only check only; no lifecycle repair apply execution and no scoped transaction apply against fixture targets occurred.
