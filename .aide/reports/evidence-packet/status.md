# EvidencePacket Status

- status: PASS
- api_version: aide.dev/v1alpha1
- protocol_version: 0.1.0
- schema_file_path: .aide/protocol/aide-evidence-packet.schema.json
- schema_file_exists: true
- schema_validation_mode: minimal_json_schema_subset
- capability_label: minimal_evidence_packet_schema
- destructive_migration_performed: false
- target_mutation: false
- provider_or_model_calls: none
- Gateway calls: none
- network_calls: none

## Supported Kinds

- EvidencePacket
- EvidencePacketProjectionReport
- EvidencePacketValidationReport

## Recognized Capabilities

- fixture_temp_apply_only
- minimal_contract_envelope
- minimal_evidence_packet_schema

## Source Reports

- lifecycle_run: true
- lifecycle_verify: true
- lifecycle_rollback: true
- lifecycle_acceptance: true
- contract_validation: true
- contract_acceptance: true

## Projection Files

- .aide/reports/evidence-packet/projections/lifecycle-fixture-run.evidence-packet.json
- .aide/reports/evidence-packet/projections/lifecycle-fixture-verify.evidence-packet.json
- .aide/reports/evidence-packet/projections/lifecycle-fixture-acceptance.evidence-packet.json
- .aide/reports/evidence-packet/projections/contract-envelope-validation.evidence-packet.json
- .aide/reports/evidence-packet/projections/contract-envelope-acceptance.evidence-packet.json
