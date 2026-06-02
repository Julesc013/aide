# Export Pack Sync

## Export Commands

- `py -3 .aide/scripts/aide_lite.py export-pack`: PASS.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS.

## Export Evidence

- Export pack: `.aide/export/aide-lite-pack-v0/**`
- Included files: 824.
- Checksum entries: 827.
- Pack status: checksum validation PASS, boundary PASS.
- Provenance: `DIRTY_SOURCE_RECORDED`.

## Managed-Section Inclusion

- Managed-section schemas, policies, examples, tests, docs, and `core/apply/**` are included in the portable pack source scope.
- `managed_section_export_pack_inclusion_golden`: PASS.

## Caveat

The dirty-source provenance is expected for this queued change because the export pack was regenerated before the AIDE-APPLY-01 commit existed.
