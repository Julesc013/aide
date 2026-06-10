# Preconditions

| Precondition | Result | Evidence |
| --- | --- | --- |
| Install dry-run checkpoint exists | PASS | `.aide/queue/AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01/` |
| Upgrade dry-run checkpoint exists | PASS | `.aide/queue/AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-CHECK-01/` |
| Repair dry-run checkpoint exists | PASS | `.aide/queue/AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01/` |
| Rollback record checkpoint exists | PASS | `.aide/queue/AIDE-LIFECYCLE-FIXTURE-ROLLBACK-RECORD-CHECK-01/` |
| Rollback dry-run checkpoint exists | PASS | `.aide/queue/AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-CHECK-01/` |
| Uninstall dry-run checkpoint exists | PASS | `.aide/queue/AIDE-LIFECYCLE-FIXTURE-UNINSTALL-DRY-RUN-CHECK-01/` |
| Static expected report inventory exists | PASS | `.aide/examples/apply/lifecycle-fixtures/expected-reports/` |
| Closure is report-only | PASS | Allowed writes exclude expected reports and fixture targets. |
