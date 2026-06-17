# Schema Review

## Result

PASS_WITH_WARNINGS

## Findings

- `.aide/protocol/aide-event-record.schema.json` parses as JSON.
- The schema declares `kind: EventRecord`.
- The top-level required fields are `apiVersion`, `kind`, `metadata`, `spec`, and `status`.
- `spec.event_ref` uses the `aide://event/<id>` form.
- `spec.subject`, `spec.causation`, `spec.correlation`, `spec.evidence_refs`, and `spec.report_refs` are modeled as ReferenceID-backed fields where practical.
- `status.recorded` is required and remains false for projected examples.
- `status.projection_only` is required and remains true.
- Helper/schema alignment reports `PASS`.

## Warnings

- Local schema validation uses the repo's minimal JSON Schema subset.
- Full JSON Schema Draft 2020-12 validation remains future work.
- Schema vocabulary does not create a runtime event store.
