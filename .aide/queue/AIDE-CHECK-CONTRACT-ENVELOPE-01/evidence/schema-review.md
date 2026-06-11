# Schema Review

Result: PASS_WITH_WARNINGS

Reviewed:

- `.aide/protocol/aide-envelope.schema.json`

Confirmed:

- JSON parses.
- Schema requires `apiVersion`, `kind`, `metadata`, `spec`, and `status`.
- `metadata`, `spec`, and `status` are object fields.
- Schema includes producer and compatibility metadata fields.
- `additionalProperties: true` preserves unknown optional extension fields.
- Schema does not define WorkUnit, EvidencePacket, TestJob, Checkpoint,
  ProviderAdapter, Service, Commander, or PromotionPolicy.
- Schema does not require destructive migration of accepted lifecycle fixture
  reports.
- Schema description states it is minimal and tied to the accepted lifecycle
  fixture runner slice.

Warning:

- The schema is a reference artifact in this slice. Runtime validation is
  performed by `core/protocol/envelope.py::validate_envelope`, not a JSON
  Schema validator. This is safe for the slice but should be hardened or
  explicitly documented before stronger protocol claims.
