# Source Chain Review

Reviewed chain:

- build: `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01`, `PASS_WITH_WARNINGS`;
- original check: `AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01`,
  `FAILED_VALIDATION`;
- repair: `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01`,
  `PASS_WITH_WARNINGS`;
- repair check: `AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-REPAIR-01`,
  `PASS_WITH_WARNINGS`;
- original acceptance: `AIDE-ACCEPT-PATCH-TRANSACTION-SCHEMA-01`, `BLOCKED`.

The repaired source chain is accepted; the original failed check and blocked
acceptance remain preserved.
