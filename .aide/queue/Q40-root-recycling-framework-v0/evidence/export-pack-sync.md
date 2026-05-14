# Export Pack Sync

## Export Result

`py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0`
completed successfully:

- included files: 366
- checksum records: 369
- boundary result: PASS
- provider/model calls: none
- network calls: none

`py -3 .aide/scripts/aide_lite.py pack-status` completed successfully:

- checksums valid: true
- boundary result: PASS
- checksum problems: 0
- provenance result during in-progress work: `DIRTY_SOURCE_RECORDED`

## Exported Q40 Portable Files

- `.aide/policies/root-recycling.yaml`
- `.aide/policies/root-inventory.yaml`
- `.aide/policies/root-fates.yaml`
- `.aide/policies/root-exceptions.yaml`
- `.aide/policies/root-risk.yaml`
- `.aide/refactors/root-inventory.schema.json`
- `.aide/refactors/root-record.schema.json`
- `.aide/refactors/root-file-classification.schema.json`
- `.aide/refactors/root-recycling-plan.schema.json`
- `.aide/refactors/root-exception.schema.json`
- `.aide/refactors/root-retirement.schema.json`
- `.aide/refactors/root-risk.schema.json`
- `.aide/roots/README.md`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q40_root_recycling.py`
- Q40 root golden tasks
- `docs/reference/root-recycling-framework.md`

## Excluded Target-Truth Outputs

The export pack includes `.aide/roots/README.md` but does not export AIDE-local
generated root inventories, classifications, plans, exceptions, or risk
summaries as target truth. Target repositories must generate their own root
outputs after import.
