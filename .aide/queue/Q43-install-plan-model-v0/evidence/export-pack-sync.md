# Export Pack Sync

## Commands

- PASS: `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0`
- PASS: `py -3 .aide/scripts/aide_lite.py pack-status`

## Pack Result

- pack: `.aide/export/aide-lite-pack-v0`
- included files: 462
- checksum count: 465
- checksums_valid: true
- boundary_result: PASS
- provenance_result: DIRTY_SOURCE_RECORDED
- boundary violations: 0

## Exported Q43 Support

The pack includes:

- `.aide/policies/install.yaml`
- `.aide/policies/install-preservation.yaml`
- `.aide/policies/install-ownership.yaml`
- `.aide/policies/install-conflicts.yaml`
- `.aide/policies/install-migrations.yaml`
- `.aide/policies/install-verification.yaml`
- `.aide/install/*.schema.json`
- `.aide/install/README.md`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q43_install_plan.py`
- Q43 install golden tasks
- `docs/reference/aide-install-model.md`
- updated `docs/reference/cross-repo-pack-export-import.md`

## Export Exclusions

The pack excludes source-generated install outputs as target truth:

- `.aide/install/latest-install-observation.*`
- `.aide/install/latest-install-plan.*`
- `.aide/install/latest-install-dry-run.*`
- `.aide/install/latest-ownership-ledger.example.json`
- `.aide/install/latest-conflict-report.*`
- `.aide/install/latest-preservation-report.md`
- `.aide/install/latest-verification-plan.md`
