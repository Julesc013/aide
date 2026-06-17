# CapabilityManifest Capabilities

- task_id: AIDE-BUILD-CAPABILITY-MANIFEST-01
- capability_target: minimal_capability_manifest
- declaration_only: true
- capabilities_count: 11
- accepted_capabilities_count: 11
- accepted_with_warnings_count: 11
- conformance_implemented: false
- admission_implemented: false
- execution_implemented: false

## Capabilities

- minimal_contract_envelope: acceptance_state=accepted_with_warnings; metadata_only=false; report_only=false; projection_only=false; runtime=false; mutating=false; admitted_by_conformance=false
- minimal_evidence_packet_schema: acceptance_state=accepted_with_warnings; metadata_only=false; report_only=false; projection_only=false; runtime=false; mutating=false; admitted_by_conformance=false
- minimal_workunit_queue_v1: acceptance_state=accepted_with_warnings; metadata_only=false; report_only=false; projection_only=true; runtime=false; mutating=false; admitted_by_conformance=false
- minimal_workunit_readonly_cli: acceptance_state=accepted_with_warnings; metadata_only=false; report_only=false; projection_only=false; runtime=false; mutating=false; admitted_by_conformance=false
- minimal_workunit_queue_metadata_mutation_cli: acceptance_state=accepted_with_warnings; metadata_only=false; report_only=false; projection_only=false; runtime=false; mutating=true; admitted_by_conformance=false
- minimal_worker_run_schema: acceptance_state=accepted_with_warnings; metadata_only=true; report_only=false; projection_only=false; runtime=false; mutating=false; admitted_by_conformance=false
- minimal_test_job_schema: acceptance_state=accepted_with_warnings; metadata_only=true; report_only=false; projection_only=false; runtime=false; mutating=false; admitted_by_conformance=false
- minimal_reference_id_scheme: acceptance_state=accepted_with_warnings; metadata_only=false; report_only=false; projection_only=true; runtime=false; mutating=false; admitted_by_conformance=false
- minimal_event_record_schema: acceptance_state=accepted_with_warnings; metadata_only=false; report_only=false; projection_only=true; runtime=false; mutating=false; admitted_by_conformance=false
- minimal_okf_knowledge_bundle: acceptance_state=accepted_with_warnings; metadata_only=false; report_only=false; projection_only=true; runtime=false; mutating=false; admitted_by_conformance=false
- minimal_reconciler_reports: acceptance_state=accepted_with_warnings; metadata_only=false; report_only=true; projection_only=false; runtime=false; mutating=false; admitted_by_conformance=false

## Warnings

- CapabilityManifest declares capability state but does not prove conformance.
- ConformanceProfile is not implemented.
- ConformanceResult is not implemented.
- Adapter admission is not implemented.
- Adapter execution is not implemented.
- Runtime capability registry is not implemented.
- PatchTransaction is not implemented.
- AdapterManifest is not implemented.
- ContextPack v2 is not implemented.
- Accepted predecessor capabilities preserve accepted_with_warnings rather than flattening to done.
- Stale latest-task-packet drift remains reported; queue truth is canonical.
