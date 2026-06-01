# Export Pack Evidence

Commands:

- `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0`
- `py -3 .aide/scripts/aide_lite.py pack-status`
- `py -3 .aide/scripts/aide_lite.py eval run --task test_telemetry_export_golden`

Results:

- Export pack regenerated at `.aide/export/aide-lite-pack-v0`.
- Boundary result: PASS.
- Included files: 673.
- Checksums valid: true.
- Provenance result: `DIRTY_SOURCE_RECORDED`.
- `test_telemetry_export_golden`: PASS, 8/8 checks.
- `.aide/tests/latest-*` generated local reports are excluded from the portable pack.
