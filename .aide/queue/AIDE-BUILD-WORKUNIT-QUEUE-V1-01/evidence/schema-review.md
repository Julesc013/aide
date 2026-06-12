# Schema Review

The schema file is `.aide/protocol/aide-workunit.schema.json`.

It requires:

- `apiVersion`
- `kind`
- `metadata`
- `spec`
- `status`

The schema is intentionally minimal and additive. It permits unknown optional fields and relies on helper validation to fail closed for unknown required capabilities.

Validation result:

- schema_file_loaded: true
- schema_file_parsed: true
- schema_validation_executed: true
- schema_validation_mode: `minimal_json_schema_subset`
- schema_helper_alignment_status: PASS
- unknown_optional_fields_tolerated: true
- unknown_required_capability_fails_closed: true
