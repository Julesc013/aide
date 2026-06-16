# Schema Review

Result: PASS_WITH_WARNINGS.

Reviewed schema:

- `.aide/protocol/aide-reference-id.schema.json`

Findings:

- Top-level required fields are `apiVersion`, `kind`, `metadata`, `spec`, and `status`.
- `kind` is constrained to `ReferenceID`.
- `metadata.compatibility` records schema/protocol/min reader/min writer versions and feature flags.
- `spec` requires `ref`, `ref_kind`, `identity`, `locator`, `required`, `relationship`, and `explicit_non_capabilities`.
- `identity` separates stable namespace/id/fragment from the locator.
- `locator` is optional metadata and may include `path`, `media_type`, `role`, and `sha256`.
- `status` records validation and syntactic resolution state.

Warnings:

- Full Draft 2020-12 JSON Schema validation remains deferred; the helper uses the repo's local minimal subset validator.
