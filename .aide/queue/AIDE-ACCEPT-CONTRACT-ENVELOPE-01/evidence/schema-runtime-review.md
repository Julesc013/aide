# Schema Runtime Review

Result: PASS

- Schema path: `.aide/protocol/aide-envelope.schema.json`
- Loaded during `contract-envelope validate`: yes.
- Parsed during `contract-envelope validate`: yes.
- Schema validation executed: yes.
- Validation mode: `minimal_json_schema_subset`.
- Helper/schema alignment checked: yes.
- Helper/schema alignment result: PASS.
- Full JSON Schema Draft 2020-12 support: explicitly deferred.

`validation.json` includes the required runtime fields:

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

The runtime path is not cosmetic: direct negative checks confirmed missing and
malformed schema cases produce non-PASS validation results.
