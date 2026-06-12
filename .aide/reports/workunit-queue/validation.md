# WorkUnit Queue Validation

- status: PASS
- api_version: aide.dev/v1alpha1
- protocol_version: 0.1.0
- schema_file_path: .aide/protocol/aide-workunit.schema.json
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
- workunit_cli_implemented: false

## Projections

- .aide/reports/workunit-queue/projections/contract-envelope-build.workunit.json
- .aide/reports/workunit-queue/projections/evidence-packet-acceptance.workunit.json
- .aide/reports/workunit-queue/projections/evidence-packet-build.workunit.json
- .aide/reports/workunit-queue/projections/lifecycle-fixture-build.workunit.json
- .aide/reports/workunit-queue/projections/workunit-queue-build.workunit.json

## Validation Results

- PASS: .aide/reports/workunit-queue/projections/contract-envelope-build.workunit.json
- PASS: .aide/reports/workunit-queue/projections/evidence-packet-acceptance.workunit.json
- PASS: .aide/reports/workunit-queue/projections/evidence-packet-build.workunit.json
- PASS: .aide/reports/workunit-queue/projections/lifecycle-fixture-build.workunit.json
- PASS: .aide/reports/workunit-queue/projections/workunit-queue-build.workunit.json

## Compatibility

- accepted_contract_envelope_preserved: true
- accepted_evidence_packet_preserved: true
- projection_paths_additive: true
- source_queue_tasks_destructively_migrated: false
- explicit_non_capabilities_preserved: true
- unknown_optional_fields_tolerated: true
- unknown_required_capability_fails_closed: true

## Schema Alignment

- alignment_errors: none

## Warnings

- WorkUnit queue v1 is minimal and v1alpha1; this is not a WorkUnit execution CLI.
- Projection outputs are additive and source queue tasks remain canonical.
- Full JSON Schema Draft 2020-12 validation remains future work.
- Work create/list/claim/block/finish/repair, WorkerRun, TestJob, Test Broker, Service, Commander, provider adapters, branch/worktree automation, target apply, rollback execution, release, and promotion remain future work.
