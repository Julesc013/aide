# AIDE-BUILD-CAPABILITY-MANIFEST-01
# Minimal AIDE CapabilityManifest Protocol Object

Create and process AIDE-BUILD-CAPABILITY-MANIFEST-01.

Use .aide/queue/index.yaml as canonical queue truth.

Goal:
Implement the first minimal CapabilityManifest protocol slice for AIDE.

This is a protocol implementation slice, not adapter execution and not conformance admission.

CapabilityManifest declares what a capability claims.
It does not prove the claim.
It does not admit the claim.
It does not execute the capability.

Core distinction:
- CapabilityManifest = declared capability
- ConformanceProfile = tests required for admission
- ConformanceResult = observed result
- Acceptance task/evidence = current repo admission record

Build only:
- CapabilityManifest schema
- helper/projection/validation
- capability manifest reports
- thin CLI dispatch if consistent with repo style
- focused tests
- queue evidence

Use accepted ReferenceID, EventRecord, OKF, and Reconciler reports where practical.

Initial capabilities to project:
- minimal_contract_envelope
- minimal_evidence_packet_schema
- minimal_workunit_queue_v1
- minimal_workunit_readonly_cli
- minimal_workunit_queue_metadata_mutation_cli
- minimal_worker_run_schema
- minimal_test_job_schema
- minimal_reference_id_scheme
- minimal_event_record_schema
- minimal_okf_knowledge_bundle
- minimal_reconciler_reports

Each manifest must distinguish:
- declared
- implemented
- checked
- accepted
- accepted_with_warnings
- metadata_only
- report_only
- projection_only
- explicit_non_capabilities
- evidence refs
- source refs
- event refs
- OKF refs
- known limitations

Non-goals:
- no ConformanceProfile
- no ConformanceResult
- no adapter admission
- no adapter execution
- no runtime
- no scheduler
- no leases
- no supervisor
- no Service
- no Commander
- no PatchTransaction
- no AdapterManifest
- no ContextPack v2
- no Test Broker runtime
- no worker execution
- no provider/model calls
- no network
- no Gateway/GitHub mutation
- no branch/worktree automation
- no target apply
- no active apply
- no release
- no production readiness
- no broad autonomous runtime behavior

Expected commands:
- py -3 .aide/scripts/aide_lite.py capability-manifest status
- py -3 .aide/scripts/aide_lite.py capability-manifest project
- py -3 .aide/scripts/aide_lite.py capability-manifest validate

Expected reports:
- .aide/reports/capability-manifest/status.md
- .aide/reports/capability-manifest/projection-report.json
- .aide/reports/capability-manifest/projection-report.md
- .aide/reports/capability-manifest/validation.json
- .aide/reports/capability-manifest/validation.md
- .aide/reports/capability-manifest/capabilities.json
- .aide/reports/capability-manifest/capabilities.md

Stop at needs_review with evidence.

Recommended next task:
AIDE-CHECK-CAPABILITY-MANIFEST-01.
