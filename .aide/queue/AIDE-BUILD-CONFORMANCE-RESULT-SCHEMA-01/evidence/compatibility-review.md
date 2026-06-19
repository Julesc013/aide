# Compatibility Review

The helper records:

- `schema_version: aide.conformance-result.v0`
- `protocol_version: 0.1.0`
- feature flag `minimal_conformance_result_schema`
- required predecessor `minimal_conformance_profile`

Compatibility is limited to deterministic parsing, projection, validation, and
indexing of the minimal result shape.

The slice does not claim compatibility for runners, execution backends, adapter
admission, PatchTransaction, runtime registries, provider calls, target apply,
release, or production use.
