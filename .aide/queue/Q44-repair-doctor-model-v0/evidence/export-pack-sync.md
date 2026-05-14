# Export Pack Sync

## Commands

- `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0`: PASS.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS.

## Pack Status

- pack: `.aide/export/aide-lite-pack-v0`
- checksums_valid: true
- boundary_result: PASS
- checksum_problems: 0
- boundary_violations: 0
- provenance_result: `DIRTY_SOURCE_RECORDED`

`DIRTY_SOURCE_RECORDED` is expected while Q44 changes are still uncommitted.

## Exported Repair Support

The export pack includes:

- `.aide/policies/repair.yaml`
- `.aide/policies/repair-classes.yaml`
- `.aide/policies/repair-safety.yaml`
- `.aide/policies/repair-detection.yaml`
- `.aide/policies/repair-verification.yaml`
- `.aide/policies/doctor.yaml`
- `.aide/repair/*.schema.json`
- `.aide/repair/README.md`
- updated `.aide/scripts/aide_lite.py`
- Q44 repair golden tasks and tests
- `docs/reference/aide-repair-model.md`
- updated install/export reference docs

## Target Truth Boundary

The pack does not export source-generated repair outputs as target truth:

- `.aide/repair/latest-repair-observation.*`: not exported.
- `.aide/repair/latest-repair-diagnosis.*`: not exported.
- `.aide/repair/latest-repair-plan.*`: not exported.
- `.aide/repair/latest-repair-dry-run.*`: not exported.
- `.aide/repair/latest-doctor-repair-report.*`: not exported.
- `.aide/repair/latest-repair-verification-plan.md`: not exported.
