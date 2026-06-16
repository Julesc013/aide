# Schema Review

Result: PASS_WITH_WARNINGS.

Reviewed schema:

- `.aide/protocol/aide-reference-id.schema.json`

Findings:

- The schema exists and declares kind `ReferenceID`.
- Top-level required fields are `apiVersion`, `kind`, `metadata`, `spec`, and `status`.
- `metadata.compatibility` records schema version, protocol version, min reader/writer versions, and feature flags.
- `spec` requires `ref`, `ref_kind`, `identity`, `locator`, `required`, `relationship`, and `explicit_non_capabilities`.
- `identity` separates namespace/id/fragment from locator metadata.
- `locator` is optional metadata and may include path, media type, role, and SHA-256.
- `status` records valid/resolution/errors/warnings.
- The schema supports stable `aide://<kind>/<id>` references and keeps file paths as locators.
- The schema does not claim runtime resolution, EventRecord, OKF, PatchTransaction, AdapterManifest, ContextPack v2, or runtime behavior.

Warning:

- Full Draft 2020-12 JSON Schema validation remains deferred. The local helper uses the same minimal JSON Schema subset pattern as nearby accepted protocol slices.

Disposition:

- Non-blocking for `minimal_reference_id_scheme` acceptance.
