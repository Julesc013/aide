# Warning Disposition

## Counts

- harmless: 0
- expected_generated_state: 2
- expected_review_gate: 3
- expected_dirty_pack_provenance: 1
- transaction_model_note: 2
- assigned_next: 1
- blocking: 0
- unknown_needs_review: 0

## Classifications

- `GENERATED-SOURCE-STALE` in `py -3 scripts/aide validate`: expected_generated_state.
- `.aide/reports/aide-apply-00-readiness.md` says `PARTIAL_NEEDS_REPAIR`: expected_generated_state; it is a stale pre-AIDE-APPLY-00 readiness report superseded by queue state, latest task packet, and current transaction reports.
- AIDE-APPLY-00 status `needs_review`: expected_review_gate.
- AIDE-CHECK-APPLY-00 status `needs_review`: expected_review_gate.
- AIDE-REVIEW-APPLY-00 status `needs_review`: expected_review_gate.
- Export pack `DIRTY_SOURCE_RECORDED`: expected_dirty_pack_provenance.
- Transaction model is fixture-only and does not implement real apply: transaction_model_note.
- Managed-section patcher is not implemented yet: transaction_model_note.
- AIDE-APPLY-01 is the next task: assigned_next.
