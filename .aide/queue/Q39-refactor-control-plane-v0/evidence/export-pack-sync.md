# Q39 Export Pack Sync

## Commands

- `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0`: PASS.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS.

## Pack Status

- included_files: 335.
- checksum_count: 338.
- checksums_valid: true.
- provenance_result: DIRTY_SOURCE_RECORDED.
- boundary_result: PASS.
- checksum_problems: 0.
- provenance_problems: 0.
- boundary_violations: 0.

## Exported Q39 Support

The pack includes portable support for:

- `.aide/policies/refactor.yaml`
- `.aide/policies/migration.yaml`
- `.aide/policies/refactor-safety.yaml`
- `.aide/policies/refactor-evidence.yaml`
- `.aide/policies/refactor-application.yaml`
- `.aide/refactors/*.schema.json`
- `.aide/refactors/README.md`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q39_refactor_control.py`
- Q39 refactor golden tasks
- `docs/reference/refactor-control-plane.md`
- adjacent Q37/Q38/export reference documentation

## Exclusions

The export pack does not export AIDE source-generated latest refactor readiness,
latest refactor plan examples, or migration-ledger example outputs as target
truth. Target repositories must generate their own refactor readiness artifacts
after import.
