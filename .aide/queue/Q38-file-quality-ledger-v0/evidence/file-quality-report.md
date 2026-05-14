# Q38 File Quality Report

## Summary

Q38 adds a deterministic, local, advisory file quality ledger that consumes the
Q37 repo intelligence outputs and writes:

- `.aide/reports/file-quality-ledger.json`
- `.aide/reports/file-quality-summary.md`
- `.aide/reports/module-quality-report.md`
- `.aide/reports/docs-consistency-report.md`
- `.aide/reports/test-coverage-map.md`
- `.aide/reports/reuse-modularity-report.md`

The ledger does not execute product work, call providers or models, mutate
branches, move files, delete files, or auto-fix source/docs/tests.

## Policy And Schema

- Policy: `.aide/policies/file-quality.yaml`
- Record schema: `.aide/quality/file-quality-record.schema.json`
- Ledger schema: `.aide/quality/file-quality-ledger.schema.json`
- Report mirror schema: `.aide/reports/file-quality-ledger.schema.json`

## Ledger Counts

- Files measured: 1589
- Quality levels:
  - exempt: 297
  - pass: 50
  - warn: 1242
- Fail count: 0

## Warning Classes

- `large_module_candidate`: 1
- `missing_doc_candidate`: 63
- `missing_test_or_validator_candidate`: 42
- `mixed_purpose_candidate`: 1
- `orphan_candidate`: 461
- `public_surface_missing_doc_candidate`: 63
- `reuse_candidate`: 274
- `stale_doc_reference_candidate`: 718
- `unknown_kind`: 146
- `unknown_owner`: 277
- `unknown_status`: 146

## Boundary Results

- Generated/evidence files are exempted or boundary-classified rather than
  treated as canonical source.
- Tracked local-state or secret-like paths would hard-fail; none were present
  in the generated ledger.
- No output recommends deletion as final truth.

## Next Action

Use these warnings as inputs for Q39 Refactor Control Plane v0. Q38 does not
decide refactors or deletions.
