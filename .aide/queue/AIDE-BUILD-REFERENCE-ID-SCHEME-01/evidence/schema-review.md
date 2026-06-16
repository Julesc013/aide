# Schema Review

Schema: `.aide/protocol/aide-reference-id.schema.json`.

Checked shape:

- Top-level fields: `apiVersion`, `kind`, `metadata`, `spec`, `status`.
- Kind enum: `ReferenceID`.
- Compatibility metadata includes schema/protocol/min reader/min writer versions and feature flags.
- Spec includes `ref`, `ref_kind`, `identity`, `locator`, `required`, `relationship`, and `explicit_non_capabilities`.
- Locator is optional metadata under the record and does not define identity.
- Status records validation and syntactic resolution state.

Known limitation:

- Local validation uses the same minimal JSON Schema subset pattern as nearby protocol slices. Full Draft 2020-12 validation remains future work.
