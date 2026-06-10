# Expected vs Actual Validation

| Check | Expected | Actual | Result |
| --- | --- | --- | --- |
| Gate selected this task | selected | selected | PASS |
| Gate authorized apply execution | true | false | FAIL_EXPECTED |
| Fixture target mutation | none when blocked | none | PASS |
| Dry-run | not run when blocked | not run | PASS |
| Apply | not run when blocked | not run | PASS |
| Next task selected | authority repair | `AIDE-LIFECYCLE-FIXTURE-INSTALL-MANAGED-SECTION-APPLY-AUTHORITY-01` | PASS |
