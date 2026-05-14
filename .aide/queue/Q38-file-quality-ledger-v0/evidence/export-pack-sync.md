# Q38 Export Pack Sync

## Export Commands

- `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0`:
  PASS.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS.

## Pack Result

- Pack path: `.aide/export/aide-lite-pack-v0`
- Included files: 301
- Checksum count: 304
- Boundary result: PASS
- Checksums valid: true
- Provenance result: `DIRTY_SOURCE_RECORDED`
- Checksum problems: 0
- Provenance problems: 0
- Boundary violations: 0

## Exported Q38 Support

The export pack now includes portable Q38 support:

- `.aide/policies/file-quality.yaml`
- `.aide/policies/docs-consistency.yaml`
- `.aide/policies/module-quality.yaml`
- `.aide/policies/reuse-modularity.yaml`
- `.aide/quality/*.schema.json`
- `.aide/quality/README.md`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q38_file_quality.py`
- Q38 golden task directories.
- `docs/reference/file-quality-ledger.md`

## Excluded Source Truth

Source-generated quality outputs were intentionally not exported as target
truth:

- `.aide/reports/file-quality-ledger.json`
- `.aide/reports/file-quality-summary.md`
- `.aide/reports/module-quality-report.md`
- `.aide/reports/docs-consistency-report.md`
- `.aide/reports/test-coverage-map.md`
- `.aide/reports/reuse-modularity-report.md`

Target repositories must run `repo inventory` and `quality ledger` locally
after import.
