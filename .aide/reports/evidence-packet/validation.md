# EvidencePacket Validation

- status: PASS
- api_version: aide.dev/v1alpha1
- protocol_version: 0.1.0
- schema_file_path: .aide/protocol/aide-evidence-packet.schema.json
- schema_file_loaded: true
- schema_file_parsed: true
- schema_validation_executed: true
- schema_validation_mode: minimal_json_schema_subset
- schema_helper_alignment_checked: true
- schema_helper_alignment_status: PASS
- destructive_migration_performed: false
- backwards_compatibility_preserved: true
- explicit_non_capabilities_preserved: true
- unknown_optional_fields_tolerated: true
- unknown_required_capability_fails_closed: true

## Projections

- .aide/reports/evidence-packet/projections/contract-envelope-acceptance.evidence-packet.json
- .aide/reports/evidence-packet/projections/contract-envelope-validation.evidence-packet.json
- .aide/reports/evidence-packet/projections/lifecycle-fixture-acceptance.evidence-packet.json
- .aide/reports/evidence-packet/projections/lifecycle-fixture-run.evidence-packet.json
- .aide/reports/evidence-packet/projections/lifecycle-fixture-verify.evidence-packet.json

## Validation Results

- PASS: .aide/reports/evidence-packet/projections/contract-envelope-acceptance.evidence-packet.json
- PASS: .aide/reports/evidence-packet/projections/contract-envelope-validation.evidence-packet.json
- PASS: .aide/reports/evidence-packet/projections/lifecycle-fixture-acceptance.evidence-packet.json
- PASS: .aide/reports/evidence-packet/projections/lifecycle-fixture-run.evidence-packet.json
- PASS: .aide/reports/evidence-packet/projections/lifecycle-fixture-verify.evidence-packet.json

## Compatibility

- accepted_reports_parse: true
- projection_paths_additive: true
- source_reports_destructively_migrated: false
- explicit_non_capabilities_preserved: true
- unknown_optional_fields_tolerated: true
- unknown_required_capability_fails_closed: true
- lifecycle_fixture_behavior_preserved: true
- contract_envelope_behavior_preserved: true

## Schema Alignment

- alignment_errors: none

## Warnings

- EvidencePacket is minimal and v1alpha1; this is not a full evidence engine.
- Projection outputs are additive and source reports remain canonical.
- Full JSON Schema Draft 2020-12 validation remains future work.
- WorkUnit, TestJob, Test Broker, Service, Commander, provider adapters, branch/worktree automation, target apply, rollback execution, release, and promotion remain future work.
