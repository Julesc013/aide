# Validation

Validation confirms the source implementation remains internally green while
the independent acceptance oracle fails:

- Source task inspect/evidence: `missing_evidence: 0`.
- OwnershipLedger `status`, `project`, and `validate`: `PASS_WITH_WARNINGS`.
- `ownership-ledger migrate-q43`: argparse refusal because the command is not
  registered.
- Check-local digest recomputation: matched source digest.
- Check-local duplicate target path probe: unexpectedly valid.
- Check-local case-fold collision probe: unexpectedly valid.
- `py_compile`: pass.
- Focused OwnershipLedger tests: 8 tests pass.
- DistributionManifest, ProjectLock, and OwnershipLedger validators:
  `PASS_WITH_WARNINGS`.
- Q43-Q48 no-apply/no-publish validators: pass.
- Broad `aide_lite.py validate`: pass.
- `git diff --check` and `git diff --cached --check`: pass.

Overall check result: `REQUEST_CHANGES`.
