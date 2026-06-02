# Export Pack Sync

Task: AIDE-APPLY-00-transaction-model

## Export Commands

- `py -3 .aide/scripts/aide_lite.py export-pack` - PASS, included_files 790, checksum_count 793, boundary_result PASS
- `py -3 .aide/scripts/aide_lite.py pack-status` - PASS, checksums_valid true, boundary_result PASS
- `transaction_export_pack_inclusion_golden` - PASS, 102/102

## Included Transaction Surfaces

- `.aide/apply/**`
- `.aide/examples/apply/**`
- `.aide/policies/transactional-apply.yaml`
- `.aide/policies/file-operations.yaml`
- `.aide/policies/transaction-safety-gates.yaml`
- `.aide/scripts/tests/test_aide_apply_00_transaction_model.py`
- `.aide/evals/golden-tasks/transaction_*_golden/**`
- `docs/reference/transaction-model.md`
- `docs/reference/transactional-apply-roadmap.md`
- `docs/reference/managed-section-operations.md`
- `docs/reference/rollback-records.md`

## Boundary

The export pack is local generated evidence. It is not a public release, target install, or source-generated target truth.
