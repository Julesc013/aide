# Schema Runtime Review

Result: PASS

Verified facts:

- schema path: `.aide/protocol/aide-envelope.schema.json`
- schema parses as JSON: yes
- runtime loads the schema during `contract-envelope validate`: yes
- runtime parses the schema during `contract-envelope validate`: yes
- minimal schema subset validation executes: yes
- validation mode: `minimal_json_schema_subset`
- full JSON Schema Draft 2020-12 compliance is not claimed
- missing schema in a temp copy returns non-PASS
- malformed schema in a temp copy returns non-PASS

Report fields reviewed in `.aide/reports/contract-envelope/validation.json`:

- `schema_file_path`
- `schema_file_exists`
- `schema_file_loaded`
- `schema_file_parsed`
- `schema_validation_executed`
- `schema_validation_mode`
- `schema_helper_alignment_checked`
- `schema_helper_alignment_status`
- `schema_validation_limitations`
- `helper_validation_errors`
- `schema_validation_errors`
- `alignment_errors`
- `unknown_optional_fields_tolerated`
- `unknown_required_capability_fails_closed`

Limitation: validation is intentionally a local subset, not a full JSON Schema
engine.
