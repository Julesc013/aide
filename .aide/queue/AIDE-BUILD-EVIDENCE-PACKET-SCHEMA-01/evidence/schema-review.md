# Schema Review

Schema path:

- `.aide/protocol/aide-evidence-packet.schema.json`

Runtime validation:

- helper validation: implemented in `core/protocol/evidence_packet.py`
- schema subset validation: implemented in `validate_evidence_packet_with_schema`
- schema/helper alignment: implemented in `check_schema_helper_alignment`

Required packet fields:

- `apiVersion`
- `kind`
- `metadata`
- `spec`
- `status`

Required `spec` fields:

- `source_task_id`
- `source_task_kind`
- `subject`
- `capability_label`
- `claims`
- `explicit_non_capabilities`
- `artifacts`
- `validations`

Current validation report:

- `.aide/reports/evidence-packet/validation.json`
- status: `PASS`
- schema_file_loaded: `true`
- schema_file_parsed: `true`
- schema_validation_executed: `true`
- schema_helper_alignment_status: `PASS`

Limitations:

- local subset validation only
- full JSON Schema Draft 2020-12 support is deferred
- no evidence engine, store, service API, or registry is implemented
