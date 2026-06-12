# WorkUnit Queue Status

- status: PASS
- api_version: aide.dev/v1alpha1
- protocol_version: 0.1.0
- schema_file_path: .aide/protocol/aide-workunit.schema.json
- schema_file_exists: true
- schema_validation_mode: minimal_json_schema_subset
- capability_label: minimal_workunit_queue_v1
- workunit_cli_implemented: false
- destructive_migration_performed: false
- target_mutation: false
- active_repo_apply_mutation: false
- provider_or_model_calls: none
- Gateway calls: none
- network_calls: none

## Supported Kinds

- WorkUnit
- WorkUnitQueueProjectionReport
- WorkUnitQueueValidationReport

## Recognized Capabilities

- fixture_temp_apply_only
- minimal_contract_envelope
- minimal_evidence_packet_schema
- minimal_workunit_queue_v1

## Source Queue Tasks

- lifecycle_fixture_build: true
- contract_envelope_build: true
- evidence_packet_build: true
- evidence_packet_acceptance: true
- workunit_queue_build: true

## Projection Files

- .aide/reports/workunit-queue/projections/lifecycle-fixture-build.workunit.json
- .aide/reports/workunit-queue/projections/contract-envelope-build.workunit.json
- .aide/reports/workunit-queue/projections/evidence-packet-build.workunit.json
- .aide/reports/workunit-queue/projections/evidence-packet-acceptance.workunit.json
- .aide/reports/workunit-queue/projections/workunit-queue-build.workunit.json
