# Prompt: AIDE-BUILD-EVENT-RECORD-SCHEMA-01

Build the narrow EventRecord schema slice after ReferenceID acceptance.

The slice must implement only schema/helper/projection/validation/thin CLI/reports/tests/queue evidence for projection-only EventRecord metadata. EventRecord must use stable `aide://...` refs from the accepted ReferenceID scheme for event identity, subject, causation, correlation, evidence, reports, and future objects where practical.

Minimum event families:

- WorkUnitStateChanged
- WorkerRunRecorded
- TestJobRecorded
- EvidencePacketRecorded
- AcceptanceRecorded
- ReferenceIDProjectionRecorded
- EventRecordProjectionRecorded
- CapabilityDeclared
- ConformanceResultRecorded
- OKFProjectionRecorded
- ReconcilerFindingRecorded
- PatchTransactionRecorded

Defining event family names does not implement those systems.

Do not implement event sourcing runtime, append-only runtime event store, runtime event log, state reconstruction, scheduler, leases, supervisor, Test Broker runtime, async execution, worker execution, Service, Commander, OKF knowledge bundle, Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, runtime reference registry, resolver service, database state, provider adapters, branch/worktree behavior, target apply, active apply, rollback/uninstall execution, release, GitHub mutation, Gateway/network/model/provider calls, production readiness, release readiness, or broad autonomous runtime.

Stop at `needs_review`. The suggested next prompt is `AIDE-CHECK-EVENT-RECORD-SCHEMA-01`; do not recommend OKF directly from this build task.
