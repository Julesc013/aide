# Token And Quality Ledger Hook

Lifecycle artifacts should reserve metadata fields for future token and quality ledger work without making cost or quality claims in this task.

## Proposed Fields

- `task_id`
- `workunit_id`
- `context_packet_id`
- `input_context_size_estimate`
- `output_plan_size_estimate`
- `validation_commands`
- `validation_status`
- `repair_or_rework_count`
- `review_status`
- `evidence_completeness`
- `unsupported_cost_claims`

## Rules

- Do not implement provider/model calls.
- Do not record credentials.
- Do not claim measured provider billing.
- Do not claim public cost savings from lifecycle schemas or fixtures.
- Do not treat estimated token counts as exact billing records.

## Future Task

`AIDE-TOKEN-QUALITY-LEDGER-01` should define how WorkUnits, ContextPackets, validation outcomes, evidence quality, rework count, and review state are recorded before AIDE makes strong lifecycle efficiency or cost-saving claims.
