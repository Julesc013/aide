# Export Pack Sync

## Commands

- `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0`: PASS after sequential rerun.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS.

## Pack Status

- checksums valid: true
- boundary result: PASS
- provenance result: DIRTY_SOURCE_RECORDED
- checksum problems: 0
- provenance problems: 0
- boundary violations: 0

## Exported Q45 Support

- `.aide/policies/upgrade.yaml`
- `.aide/policies/upgrade-compatibility.yaml`
- `.aide/policies/upgrade-preservation.yaml`
- `.aide/policies/upgrade-conflicts.yaml`
- `.aide/policies/upgrade-migrations.yaml`
- `.aide/policies/upgrade-verification.yaml`
- `.aide/upgrade/README.md`
- `.aide/upgrade/*.schema.json`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q45_upgrade_model.py`
- `.aide/evals/golden-tasks/catalog.yaml`
- `docs/reference/aide-upgrade-model.md`
- related install/repair/export documentation updates.

## Exclusions

The export pack includes portable upgrade support, not AIDE-source generated upgrade truth. The pack does not include:

- `.aide/upgrade/latest-current-install-observation.*`
- `.aide/upgrade/latest-source-pack-observation.*`
- `.aide/upgrade/latest-upgrade-comparison.*`
- `.aide/upgrade/latest-upgrade-plan.*`
- `.aide/upgrade/latest-upgrade-dry-run.*`
- `.aide/upgrade/latest-upgrade-conflict-report.*`
- `.aide/upgrade/latest-upgrade-migration-report.md`
- `.aide/upgrade/latest-upgrade-compatibility-report.md`
- `.aide/upgrade/latest-upgrade-verification-plan.md`
