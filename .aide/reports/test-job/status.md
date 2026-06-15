# TestJob Status

- status: PASS
- api_version: aide.dev/v1alpha1
- protocol_version: 0.1.0
- schema_file_path: .aide/protocol/aide-test-job.schema.json
- schema_file_exists: true
- schema_validation_mode: minimal_json_schema_subset
- capability_label: minimal_test_job_schema
- implementation_scope: schema_helper_projection_cli_only
- accepted_predecessor: minimal_worker_run_schema
- test_broker_runtime_implemented: false
- async_test_execution_implemented: false
- test_job_submission_implemented: false
- test_job_run_implemented: false
- scheduler_implemented: false
- leases_implemented: false
- supervisor_implemented: false
- worker_execution_implemented: false
- workunit_claim_run_finish_repair_implemented: false
- provider_adapter_implemented: false
- service_implemented: false
- commander_implemented: false
- destructive_migration_performed: false
- target_mutation: false
- active_repo_apply_mutation: false
- branch_mutation: false
- provider_or_model_calls: none
- Gateway calls: none
- network_calls: none
- github_mutation: false

## Supported Kinds

- TestJob
- TestJobProjectionReport
- TestJobValidationReport

## Source Reports

- worker_run_acceptance: true
- worker_run_check: true
- worker_run_validation: true
- workunit_cli_mutation_acceptance: true
- workunit_cli_mutation_check: true
- workunit_cli_acceptance: true
- workunit_queue_acceptance: true
- evidence_packet_validation: true
- contract_envelope_validation: true

## Projection Files

- .aide/reports/test-job/projections/worker-run-acceptance.test-job.json
- .aide/reports/test-job/projections/worker-run-check.test-job.json
- .aide/reports/test-job/projections/worker-run-validation.test-job.json
- .aide/reports/test-job/projections/workunit-cli-mutation-acceptance.test-job.json
- .aide/reports/test-job/projections/workunit-cli-mutation-check.test-job.json
- .aide/reports/test-job/projections/workunit-cli-acceptance.test-job.json
- .aide/reports/test-job/projections/workunit-queue-acceptance.test-job.json
- .aide/reports/test-job/projections/evidence-packet-validation.test-job.json
- .aide/reports/test-job/projections/contract-envelope-validation.test-job.json

## Non-Capabilities

- test_broker_runtime
- async_test_execution
- test_job_submission
- test_job_run
- test_job_retry_runtime
- test_job_summarize_runtime
- scheduler
- leases
- supervisor
- worker_execution
- workunit_claim
- workunit_run
- workunit_finish
- workunit_repair
- service
- commander
- provider_adapters
- branch_worktree_automation
- target_apply
- active_apply
- rollback_execution
- uninstall_execution
- release
- promotion
- gateway
- network
- github_mutation
- model_provider_calls
- production_ready
- release_ready
