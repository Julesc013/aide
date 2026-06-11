# Contract Envelope Validation

- status: PASS
- api_version: aide.dev/v1alpha1
- protocol_version: 0.1.0
- schema_file_path: .aide/protocol/aide-envelope.schema.json
- schema_file_loaded: true
- schema_file_parsed: true
- schema_validation_executed: true
- schema_validation_mode: minimal_json_schema_subset
- schema_helper_alignment_checked: true
- schema_helper_alignment_status: PASS
- destructive_migration_performed: false
- backwards_compatibility_preserved: true
- unknown_optional_fields_tolerated: true
- unknown_required_capability_fails_closed: true

## Projections

- .aide/reports/contract-envelope/projections/lifecycle-fixture-acceptance.envelope.json
- .aide/reports/contract-envelope/projections/lifecycle-fixture-latest-run.envelope.json
- .aide/reports/contract-envelope/projections/lifecycle-fixture-verify.envelope.json

## Validation Results

- PASS: .aide/reports/contract-envelope/projections/lifecycle-fixture-acceptance.envelope.json
- PASS: .aide/reports/contract-envelope/projections/lifecycle-fixture-latest-run.envelope.json
- PASS: .aide/reports/contract-envelope/projections/lifecycle-fixture-verify.envelope.json

## Compatibility

- latest_run_json_parses: true
- verify_json_parses: true
- latest_run_top_level_status_scalar_preserved: true
- verify_top_level_status_scalar_preserved: true
- latest_run_legacy_capability_label_preserved: true
- verify_legacy_capability_label_preserved: true
- source_reports_destructively_migrated: false

## Schema Alignment

- alignment_errors: none

## Schema Validation Limitations

- Local subset validator supports type, required, properties, simple additionalProperties, and homogeneous array items only.
- Full JSON Schema Draft 2020-12 validation remains future work.
- Formats, refs, oneOf/anyOf/allOf, conditionals, numeric bounds, and pattern checks are not implemented.

## Warnings

- Minimal envelope helper is v1alpha1 and is not a full protocol stability claim.
- Minimal schema subset validation is executed; full JSON Schema Draft 2020-12 validation remains future work.
- WorkUnit, EvidencePacket, TestJob, Checkpoint, ProviderAdapter, Service, and Commander schemas remain future work.
