# Schema Review

Result: PASS_WITH_WARNINGS.

Accepted:

- `.aide/protocol/aide-test-job.schema.json` exists and parses as JSON.
- The schema declares `kind: TestJob`.
- The schema uses the public `apiVersion`, `kind`, `metadata`, `spec`, and `status` shape.
- The schema includes compatibility metadata, command/cwd/environment policy metadata, framework metadata, timeout metadata, artifact/log references, EvidencePacket references, failure-summary placeholders, retry/flake placeholders, and explicit non-capability metadata.
- Required status metadata includes phase, result, validation state, validation errors, and validation warnings.
- Nullable start/end/exit/duration metadata is present.

Warning: validation remains limited to the accepted local minimal JSON Schema subset. Full Draft 2020-12 validation is deferred and is not accepted as present capability.
