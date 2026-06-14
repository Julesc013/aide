# WorkerRun Validation

- status: PASS
- capability_label: minimal_worker_run_schema
- api_version: aide.dev/v1alpha1
- protocol_version: 0.1.0
- schema_file_path: .aide/protocol/aide-worker-run.schema.json
- schema_file_loaded: true
- schema_file_parsed: true
- schema_validation_executed: true
- schema_validation_mode: minimal_json_schema_subset
- schema_helper_alignment_checked: true
- schema_helper_alignment_status: PASS
- worker_execution_implemented: false
- worker_execution_performed: false
- workunit_claim_implemented: false
- workunit_run_implemented: false
- worker_lease_implemented: false
- scheduler_implemented: false
- provider_adapter_implemented: false
- testjob_schema_implemented: false
- test_broker_implemented: false
- destructive_migration_performed: false
- backwards_compatibility_preserved: true
- source_reports_mutated: false
- explicit_non_capabilities_preserved: true
- unknown_optional_fields_tolerated: true
- unknown_required_capability_fails_closed: true

## Projections

- .aide/reports/worker-run/projections/workunit-cli-mutation-acceptance.worker-run.json
- .aide/reports/worker-run/projections/workunit-cli-mutation-check.worker-run.json
- .aide/reports/worker-run/projections/workunit-cli-mutation-validation.worker-run.json
- .aide/reports/worker-run/projections/workunit-cli-validation.worker-run.json
- .aide/reports/worker-run/projections/workunit-queue-validation.worker-run.json

## Validation Results

- PASS: .aide/reports/worker-run/projections/workunit-cli-mutation-acceptance.worker-run.json
- PASS: .aide/reports/worker-run/projections/workunit-cli-mutation-check.worker-run.json
- PASS: .aide/reports/worker-run/projections/workunit-cli-mutation-validation.worker-run.json
- PASS: .aide/reports/worker-run/projections/workunit-cli-validation.worker-run.json
- PASS: .aide/reports/worker-run/projections/workunit-queue-validation.worker-run.json

## Compatibility

- status: pass
- accepted_reports_parse: true
- lifecycle_fixture_behavior_preserved: true
- contract_envelope_behavior_preserved: true
- evidence_packet_behavior_preserved: true
- workunit_queue_behavior_preserved: true
- workunit_cli_behavior_preserved: true
- workunit_cli_mutation_behavior_preserved: true
- destructive_migration_performed: false
- projection_paths_additive: true

## Schema Alignment

- alignment_errors: none

## Warnings

- WorkerRun is a minimal v1alpha1 data schema; worker execution is not implemented.
- Projection outputs are additive and source reports remain canonical.
- Full JSON Schema Draft 2020-12 validation remains future work.
- WorkUnit claim/run/finish/repair, leases, scheduler, TestJob, Test Broker, Service, Commander, provider adapters, branch/worktree automation, target apply, rollback execution, release, and promotion remain future work.
