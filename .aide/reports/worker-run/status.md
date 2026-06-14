# WorkerRun Status

- status: PASS
- api_version: aide.dev/v1alpha1
- protocol_version: 0.1.0
- schema_file_path: .aide/protocol/aide-worker-run.schema.json
- schema_file_exists: true
- schema_validation_mode: minimal_json_schema_subset
- capability_label: minimal_worker_run_schema
- worker_execution_implemented: false
- workunit_claim_implemented: false
- workunit_run_implemented: false
- worker_lease_implemented: false
- scheduler_implemented: false
- provider_adapter_implemented: false
- testjob_schema_implemented: false
- test_broker_implemented: false
- destructive_migration_performed: false
- target_mutation: false
- active_repo_apply_mutation: false
- provider_or_model_calls: none
- Gateway calls: none
- network_calls: none

## Supported Kinds

- WorkerRun
- WorkerRunProjectionReport
- WorkerRunValidationReport

## Source Reports

- workunit_cli_mutation_validation: true
- workunit_cli_mutation_check: true
- workunit_cli_mutation_acceptance: true
- workunit_cli_validation: true
- workunit_queue_validation: true

## Projection Files

- .aide/reports/worker-run/projections/workunit-cli-mutation-validation.worker-run.json
- .aide/reports/worker-run/projections/workunit-cli-mutation-check.worker-run.json
- .aide/reports/worker-run/projections/workunit-cli-mutation-acceptance.worker-run.json
- .aide/reports/worker-run/projections/workunit-cli-validation.worker-run.json
- .aide/reports/worker-run/projections/workunit-queue-validation.worker-run.json
