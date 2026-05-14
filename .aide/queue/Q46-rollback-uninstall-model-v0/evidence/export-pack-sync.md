# Export Pack Sync

Command: `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0`

- Result: PASS.
- Included files: 555.
- Checksums: 558.
- Boundary result: PASS.
- Provider/model calls: none.
- Network calls: none.

Command: `py -3 .aide/scripts/aide_lite.py pack-status`

- Result: PASS.
- Checksums valid: true.
- Boundary result: PASS.
- Provenance result: `DIRTY_SOURCE_RECORDED`.

Exported rollback/uninstall support includes:

- `.aide/policies/rollback*.yaml`
- `.aide/policies/uninstall*.yaml`
- `.aide/rollback/*.schema.json`
- `.aide/rollback/README.md`
- `.aide/uninstall/*.schema.json`
- `.aide/uninstall/README.md`
- updated `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q46_rollback_uninstall.py`
- Q46 golden tasks and catalog entries
- `docs/reference/aide-rollback-uninstall.md`

Excluded as target truth:

- `.aide/rollback/latest-*`
- `.aide/uninstall/latest-*`

Search verification found only documentation references to latest rollback and
uninstall output paths inside the export pack, not exported latest output files.
