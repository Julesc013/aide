# Validation Results

- Source task inspect/evidence: `missing_evidence: 0`.
- OwnershipLedger `status`, `project`, and `validate`: `PASS_WITH_WARNINGS`.
- `ownership-ledger migrate-q43`: failed through argparse because the subcommand
  is not implemented.
- Check-local digest recomputation matched
  `sha256:a7c005b549fc66c97373377cf24c28d551f1ffd3fa79370cd76708c935083b08`.
- Check-local required field probe showed required file-entry and
  managed-section fields are absent.
- Check-local duplicate target path probe validated with no refusal.
- Check-local case-fold collision probe validated with no refusal.
- `py_compile`: pass.
- Focused OwnershipLedger unittest suite: 8 tests pass.
- DistributionManifest, ProjectLock, OwnershipLedger validators:
  `PASS_WITH_WARNINGS`.
- Q43-Q48 no-apply/no-publish validators executed and passed.
- Broad `aide_lite.py validate`: `PASS`.

Overall check result: `REQUEST_CHANGES`.
