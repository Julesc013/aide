# Capability Inventory Review

Finding: pass with warnings.

Required capabilities projected:

- `minimal_contract_envelope`
- `minimal_evidence_packet_schema`
- `minimal_workunit_queue_v1`
- `minimal_workunit_readonly_cli`
- `minimal_workunit_queue_metadata_mutation_cli`
- `minimal_worker_run_schema`
- `minimal_test_job_schema`
- `minimal_reference_id_scheme`
- `minimal_event_record_schema`
- `minimal_okf_knowledge_bundle`
- `minimal_reconciler_reports`

Observed status semantics:

- accepted_with_warnings: `11`
- metadata_only: `minimal_worker_run_schema`, `minimal_test_job_schema`
- report_only: `minimal_reconciler_reports`
- projection_only: `minimal_workunit_queue_v1`,
  `minimal_reference_id_scheme`, `minimal_event_record_schema`,
  `minimal_okf_knowledge_bundle`
- mutating: `minimal_workunit_queue_metadata_mutation_cli`
- runtime true: none
- admitted_by_conformance true: none

All capability records include source, evidence, report, event, and explicit
non-capability refs. OKF refs are attached where the corresponding OKF pages
exist.
