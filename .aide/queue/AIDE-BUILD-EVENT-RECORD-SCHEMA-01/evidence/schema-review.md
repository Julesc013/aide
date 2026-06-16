# Schema Review

## Result

PASS_WITH_WARNINGS

## Findings

- `.aide/protocol/aide-event-record.schema.json` parses as JSON.
- The schema declares `kind: EventRecord`.
- The top-level required fields are `apiVersion`, `kind`, `metadata`, `spec`, and `status`.
- `spec.event_ref` uses the `aide://event/<id>` identity form.
- `spec.subject`, `spec.causation`, `spec.correlation`, `spec.evidence_refs`, and `spec.report_refs` are modeled as ReferenceID-backed fields where practical.
- `spec.causation` and `spec.correlation` are optional object-or-null fields.
- `status.recorded` is required and remains false for this projection-only slice.
- `status.projection_only` is required and remains true.

## Warnings

- Full JSON Schema Draft 2020-12 validation remains deferred; the helper performs the repo's existing minimal subset validation.
- Schema vocabulary does not create a runtime event store.
