# AIDE-CHECK-OWNERSHIP-LEDGER-V1-REPAIR-01

Create and process a check-only independent review of `AIDE-BUILD-OWNERSHIP-LEDGER-V1-REPAIR-01`.

Verify that the repair closes exactly:

- `ownership.file_entry_contract_incomplete`
- `ownership.managed_section_contract_incomplete`
- `ownership.q43_migration_missing`
- `ownership.conflict_model_incomplete`
- `ownership.fixture_coverage_incomplete`

Do not repair implementation.
Do not accept OwnershipLedger v1.
Do not begin InstallRecord, MigrationRecord, UpdatePlan, RollbackBundle, apply-engine, canaries, target-repository work, publication, runtime, provider/model/network behavior, Workbench/MCP, source-change preview/apply/rollback, or promotion.

Stop at `needs_review`.

If all material checks pass, recommend exactly:

```text
AIDE-ACCEPT-OWNERSHIP-LEDGER-V1-01
```

If a material defect remains, recommend exactly:

```text
AIDE-BUILD-OWNERSHIP-LEDGER-V1-REPAIR-02
```
