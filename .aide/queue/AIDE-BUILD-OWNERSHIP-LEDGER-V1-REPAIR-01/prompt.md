# AIDE-BUILD-OWNERSHIP-LEDGER-V1-REPAIR-01

Create and process a bounded repair for the five material findings from `AIDE-CHECK-OWNERSHIP-LEDGER-V1-01`.

Repair exactly:

- `ownership.file_entry_contract_incomplete`
- `ownership.managed_section_contract_incomplete`
- `ownership.q43_migration_missing`
- `ownership.conflict_model_incomplete`
- `ownership.fixture_coverage_incomplete`

Stop at `needs_review`, preserve failed history, and recommend exactly:

```text
AIDE-CHECK-OWNERSHIP-LEDGER-V1-REPAIR-01
```

Do not accept OwnershipLedger v1 or begin downstream distribution objects.
