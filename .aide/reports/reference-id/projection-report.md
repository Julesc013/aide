# ReferenceID Projection

- status: PASS_WITH_WARNINGS
- task_id: AIDE-BUILD-REFERENCE-ID-SCHEME-01
- capability_target: minimal_reference_id_scheme
- projected_refs_count: 25
- scheme: aide
- grammar: aide://<kind>/<id>
- file_paths_are_locators: true
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
- recommended_next_task: AIDE-CHECK-REFERENCE-ID-SCHEME-01

## Source Artifacts Checked

- .aide/queue/AIDE-ACCEPT-TESTJOB-SCHEMA-01/task.yaml
- .aide/queue/AIDE-CHECK-TESTJOB-SCHEMA-01/task.yaml
- .aide/queue/AIDE-BUILD-TESTJOB-SCHEMA-01/task.yaml
- .aide/queue/AIDE-ACCEPT-WORKER-RUN-SCHEMA-01/task.yaml
- .aide/protocol/aide-envelope.schema.json
- .aide/protocol/aide-evidence-packet.schema.json
- .aide/protocol/aide-workunit.schema.json
- .aide/protocol/aide-worker-run.schema.json
- .aide/protocol/aide-test-job.schema.json
- .aide/protocol/aide-reference-id.schema.json
- .aide/reports/contract-envelope/validation.json
- .aide/reports/evidence-packet/validation.json
- .aide/reports/workunit-queue/validation.json
- .aide/reports/worker-run-accept/acceptance-report.json
- .aide/reports/test-job-accept/acceptance-report.json
- .aide/reports/test-job-accept/acceptance-report.json
- .aide/reports/test-job-check/check-report.json
- .aide/reports/test-job/validation.json
- .aide/queue/AIDE-ACCEPT-TESTJOB-SCHEMA-01/evidence/acceptance-summary.md
- .aide/queue/AIDE-ACCEPT-TESTJOB-SCHEMA-01/evidence/warning-disposition.md
- .aide/queue/AIDE-ACCEPT-TESTJOB-SCHEMA-01/evidence/non-capability-boundary.md

## Reports Written

- .aide/reports/reference-id/projection-report.json
- .aide/reports/reference-id/projection-report.md
- .aide/reports/reference-id/reference-map.json
- .aide/reports/reference-id/reference-map.md

## Warnings

- Reference ID Scheme is syntactic/projection-only and does not implement runtime resolution.
- Future ref kinds may be syntactically valid without implementing their object protocols.
