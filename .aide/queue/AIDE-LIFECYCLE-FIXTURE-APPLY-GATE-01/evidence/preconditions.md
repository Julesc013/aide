# Preconditions

| Precondition | Result | Evidence |
| --- | --- | --- |
| Scoped transaction executor accepted with notes | PASS | `AIDE-APPLY-02-REPAIR-01` and `AIDE-CHECK-APPLY-02-RECHECK-01` |
| Lifecycle dry-run proof closure completed | PASS | `AIDE-LIFECYCLE-FIXTURE-PROOF-CLOSURE-01` |
| Static expected report gap repair completed | PASS_WITH_WARNINGS | `AIDE-LIFECYCLE-EXPECTED-REPORT-GAP-REPAIR-01`; embedded generated-plan refs for repaired scenarios remain deferred |
| Candidate generated plan exists | PASS | `install-managed-section.plan.json` |
| Candidate expected report exists | PASS | `install-managed-section.report.json` |
| Candidate rollback record exists | PASS | `install-managed-section.rollback.json` |
| Apply execution authorized by this gate | FAIL_EXPECTED | This gate is planning-only and does not authorize apply. |
