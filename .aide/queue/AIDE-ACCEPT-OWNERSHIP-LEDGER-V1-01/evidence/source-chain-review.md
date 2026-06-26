# Source Chain Review

The OwnershipLedger v1 source chain is complete and review-gated:

- `AIDE-BUILD-OWNERSHIP-LEDGER-V1-01`
  - commit: `37bb014ce3f43e0818fa391c03fb86ac012d34ad`
  - result: `PASS_WITH_WARNINGS`
  - material findings: `0`
  - missing evidence: `0`
- `AIDE-CHECK-OWNERSHIP-LEDGER-V1-01`
  - commit: `96ba39104542fd68aa877a302de8dfccef14ab1d`
  - result: `REQUEST_CHANGES`
  - material findings: `5`
  - missing evidence: `0`
- `AIDE-BUILD-OWNERSHIP-LEDGER-V1-REPAIR-01`
  - commit: `d466004625bdd8d17998ad325bb6b124e236562c`
  - result: `PASS_WITH_WARNINGS`
  - material findings: `0`
  - missing evidence: `0`
- `AIDE-CHECK-OWNERSHIP-LEDGER-V1-REPAIR-01`
  - commit: `ab58ccb1123d83ecf2e0238a9cf538ca40ab7e41`
  - result: `PASS_WITH_WARNINGS`
  - material findings: `0`
  - missing evidence: `0`
  - recommended next task: `AIDE-ACCEPT-OWNERSHIP-LEDGER-V1-01`

The five original material findings are closed by repair evidence and
independently verified by the repair check:

- `ownership.file_entry_contract_incomplete`
- `ownership.managed_section_contract_incomplete`
- `ownership.q43_migration_missing`
- `ownership.conflict_model_incomplete`
- `ownership.fixture_coverage_incomplete`
