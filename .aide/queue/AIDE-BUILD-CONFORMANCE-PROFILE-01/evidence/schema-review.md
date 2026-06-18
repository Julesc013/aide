# Schema Review

The schema at `.aide/protocol/aide-conformance-profile.schema.json` uses the
existing AIDE envelope pattern:

- `apiVersion`
- `kind`
- `metadata`
- `spec`
- `status`

The schema constrains `kind` to `ConformanceProfile` and requires the profile
identity, version, lifecycle, subject, profile classes, cases, aggregation
policy, evidence requirements, and explicit non-capabilities.

The schema is intentionally minimal. Runtime JSON Schema Draft 2020-12 features
remain future work; the helper performs local structural validation for the
fields needed by this slice.
