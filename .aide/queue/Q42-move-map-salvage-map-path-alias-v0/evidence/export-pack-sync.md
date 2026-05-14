# Export Pack Sync

## Export Command

- `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0`: PASS.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS.

## Pack Result

- Pack path: `.aide/export/aide-lite-pack-v0`
- Included files: 426
- Checksums: 429
- Checksums valid: true
- Boundary result: PASS
- Provenance result: `DIRTY_SOURCE_RECORDED`
- Boundary violations: 0

## Portable Q42 Files Exported

- `.aide/policies/move-map.yaml`
- `.aide/policies/salvage-map.yaml`
- `.aide/policies/path-aliases.yaml`
- `.aide/policies/reference-rewrite.yaml`
- `.aide/policies/migration-ledger.yaml`
- `.aide/refactors/move-map.schema.json`
- `.aide/refactors/move-map-entry.schema.json`
- `.aide/refactors/salvage-map.schema.json`
- `.aide/refactors/salvage-map-entry.schema.json`
- `.aide/refactors/path-aliases.schema.json`
- `.aide/refactors/path-alias-entry.schema.json`
- `.aide/refactors/path-aliases.template.yaml`
- `.aide/refactors/reference-rewrite-plan.schema.json`
- `.aide/refactors/reference-rewrite-entry.schema.json`
- `.aide/refactors/migration-ledger.schema.json`
- `.aide/refactors/migration-ledger-entry.schema.json`
- `.aide/refactors/map-validation-report.schema.json`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q42_move_map_aliases.py`
- Q42 golden task packets and catalog entries.
- `docs/reference/move-salvage-path-aliases.md`

## Source-Generated Outputs Excluded As Target Truth

The export report records `source_repo_current_map_outputs` as an excluded
class. The pack does not export source-generated current maps as target truth:

- `.aide/refactors/current-move-map.*`
- `.aide/refactors/current-salvage-map.*`
- `.aide/refactors/path-aliases.yaml`
- `.aide/refactors/path-aliases.md`
- `.aide/refactors/reference-rewrite-plan.*`
- `.aide/refactors/migration-ledger.draft.jsonl`
- `.aide/refactors/map-validation-report.*`
