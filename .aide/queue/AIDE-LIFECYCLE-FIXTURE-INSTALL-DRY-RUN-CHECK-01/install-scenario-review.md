# Install Scenario Review

| Scenario | State | Expected Status | Expected Blocker | Expected Report | Path Boundary | Managed Section | Hash | Mutation State |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| install-clean | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | missing ref, generated report used | PASS | not applicable | not applicable | PASS |
| install-existing-manual-preserved | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | missing ref, generated report used | PASS | PASS | not applicable | PASS |
| install-managed-section | PASS | PASS_WITH_WARNINGS | none | present | PASS | PASS | PASS | PASS |
| protected-path-blocked | PASS | BLOCKED | BLOCKED_PROTECTED_PATH | present | PASS | not applicable | not applicable | PASS |
| traversal-blocked | PASS | BLOCKED | BLOCKED_PATH_TRAVERSAL | present | PASS | not applicable | not applicable | PASS |

All five install scenarios were reviewed. The missing static expected report refs are non-blocking for checkpoint acceptance and remain a documented evidence gap.
