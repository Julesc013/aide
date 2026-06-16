# ReferenceID Validation

- status: PASS_WITH_WARNINGS
- validation_status: PASS_WITH_WARNINGS
- capability_target: minimal_reference_id_scheme
- schema_path: .aide/protocol/aide-reference-id.schema.json
- schema_exists: true
- helper_path: core/protocol/reference_id.py
- helper_exists: true
- cli_registered: true
- projection_generated: true
- reference_map_json_valid: true
- all_projected_refs_parse: true
- required_locators_exist: true
- sha256_checked: true
- predecessor_compatibility_preserved: true
- overclaiming_check_passed: true
- forbidden_ops_preserved: true
- unknown_optional_ref_kind_warned: true
- unknown_required_ref_kind_fails_closed: true
- runtime_reference_registry_implemented: false
- resolver_service_implemented: false
- event_record_implemented: false
- okf_knowledge_bundle_implemented: false
- patch_transaction_implemented: false
- adapter_manifest_implemented: false
- target_mutation: false
- active_repo_apply_mutation: false
- branch_mutation: false
- provider_or_model_calls: none
- Gateway calls: none
- network_calls: none
- github_mutation: false

## Validation Results

- PASS: aide://queue-task/AIDE-ACCEPT-TESTJOB-SCHEMA-01
- PASS: aide://queue-task/AIDE-CHECK-TESTJOB-SCHEMA-01
- PASS: aide://queue-task/AIDE-BUILD-TESTJOB-SCHEMA-01
- PASS: aide://queue-task/AIDE-ACCEPT-WORKER-RUN-SCHEMA-01
- PASS: aide://schema/envelope
- PASS: aide://schema/evidence-packet
- PASS: aide://schema/workunit
- PASS: aide://schema/worker-run
- PASS: aide://schema/test-job
- PASS: aide://schema/reference-id
- PASS: aide://capability/minimal_contract_envelope
- PASS: aide://capability/minimal_evidence_packet_schema
- PASS: aide://capability/minimal_workunit_queue_v1
- PASS: aide://capability/minimal_worker_run_schema
- PASS: aide://capability/minimal_test_job_schema
- PASS: aide://report/test-job-acceptance-report
- PASS: aide://report/test-job-check-report
- PASS: aide://report/test-job-validation
- PASS: aide://report/reference-id-projection-report
- PASS: aide://report/reference-id-validation
- PASS: aide://evidence/aide-accept-testjob-schema-01-acceptance-summary
- PASS: aide://evidence/aide-accept-testjob-schema-01-warning-disposition
- PASS: aide://evidence/aide-accept-testjob-schema-01-non-capability-boundary
- PASS: aide://event/future-event-placeholder
- PASS: aide://patch-transaction/future-patch-transaction-placeholder

## Warnings

- Reference ID Scheme is syntactic/projection-only and does not implement runtime resolution.
- EventRecord is not implemented.
- OKF knowledge bundle is not implemented.
- PatchTransaction is not implemented by this task.
- Runtime registry/resolver service is not implemented.
