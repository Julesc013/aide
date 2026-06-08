# Install Scenario Matrix

| Scenario | Check State | Expected Status | Expected Blocker | Path Boundary | Managed Section | Hash | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| install-clean | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | PASS | NOT_APPLICABLE | PASS | static expected report ref absent; generated plan report used |
| install-existing-manual-preserved | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | PASS | PASS | PASS | static expected report ref absent; generated plan report used |
| install-managed-section | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | PASS | PASS | PASS | fixture metadata expects PASS_WITH_WARNINGS |
| protected-path-blocked | PASS | BLOCKED | BLOCKED_PROTECTED_PATH | PASS | NOT_APPLICABLE | PASS | protected path metadata blocks before mutation |
| traversal-blocked | PASS | BLOCKED | BLOCKED_PATH_TRAVERSAL | PASS | NOT_APPLICABLE | PASS | traversal metadata blocks before mutation |

Residual risk for all scenarios: static report-only check only; no lifecycle dry-run harness execution and no install apply execution occurred.
