# TestJob Validation

- status: PASS
- capability_label: minimal_test_job_schema
- api_version: aide.dev/v1alpha1
- protocol_version: 0.1.0
- schema_file_path: .aide/protocol/aide-test-job.schema.json
- helper_path: core/protocol/test_job.py
- schema_file_loaded: true
- schema_file_parsed: true
- schema_validation_executed: true
- schema_validation_mode: minimal_json_schema_subset
- schema_helper_alignment_checked: true
- schema_helper_alignment_status: PASS
- test_broker_runtime_implemented: false
- async_test_execution_implemented: false
- test_job_submission_implemented: false
- test_job_run_implemented: false
- worker_execution_implemented: false
- workunit_claim_run_finish_repair_implemented: false
- scheduler_implemented: false
- leases_implemented: false
- provider_adapter_implemented: false
- service_implemented: false
- commander_implemented: false
- destructive_migration_performed: false
- backwards_compatibility_preserved: true
- source_reports_mutated: false
- explicit_non_capabilities_preserved: true
- unknown_optional_fields_tolerated: true
- unknown_required_capability_fails_closed: true

## Projections

- .aide/reports/test-job/projections/contract-envelope-validation.test-job.json
- .aide/reports/test-job/projections/evidence-packet-validation.test-job.json
- .aide/reports/test-job/projections/worker-run-acceptance.test-job.json
- .aide/reports/test-job/projections/worker-run-check.test-job.json
- .aide/reports/test-job/projections/worker-run-validation.test-job.json
- .aide/reports/test-job/projections/workunit-cli-acceptance.test-job.json
- .aide/reports/test-job/projections/workunit-cli-mutation-acceptance.test-job.json
- .aide/reports/test-job/projections/workunit-cli-mutation-check.test-job.json
- .aide/reports/test-job/projections/workunit-queue-acceptance.test-job.json

## Validation Results

- PASS: .aide/reports/test-job/projections/contract-envelope-validation.test-job.json
- PASS: .aide/reports/test-job/projections/evidence-packet-validation.test-job.json
- PASS: .aide/reports/test-job/projections/worker-run-acceptance.test-job.json
- PASS: .aide/reports/test-job/projections/worker-run-check.test-job.json
- PASS: .aide/reports/test-job/projections/worker-run-validation.test-job.json
- PASS: .aide/reports/test-job/projections/workunit-cli-acceptance.test-job.json
- PASS: .aide/reports/test-job/projections/workunit-cli-mutation-acceptance.test-job.json
- PASS: .aide/reports/test-job/projections/workunit-cli-mutation-check.test-job.json
- PASS: .aide/reports/test-job/projections/workunit-queue-acceptance.test-job.json

## Compatibility

- status: pass
- accepted_reports_parse: true
- contract_envelope_behavior_preserved: true
- evidence_packet_behavior_preserved: true
- workunit_queue_behavior_preserved: true
- worker_run_behavior_preserved: true
- worker_run_acceptance_preserved: true
- testjob_does_not_require_worker_execution: true
- testjob_does_not_require_test_broker_runtime: true
- projection_paths_additive: true
- destructive_migration_performed: false

## Schema Alignment

- alignment_errors: none

## Warnings

- TestJob is a minimal v1alpha1 metadata schema; Test Broker runtime is not implemented.
- Projection outputs are additive and source reports remain canonical.
- Full JSON Schema Draft 2020-12 validation remains future work.
- WorkUnit claim/run/finish/repair, leases, scheduler, worker execution, Test Broker, Service, Commander, provider adapters, branch/worktree automation, target apply, rollback execution, release, and promotion remain future work.
