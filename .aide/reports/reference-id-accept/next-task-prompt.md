# AIDE-BUILD-EVENT-RECORD-SCHEMA-01
# Append-Only AIDE EventRecord Schema

Create and process AIDE-BUILD-EVENT-RECORD-SCHEMA-01.

Goal:
Implement the first minimal EventRecord protocol slice for AIDE.

This is a protocol implementation slice, not a runtime event store.

Build only:
- EventRecord schema
- helper
- validation
- deterministic projection/report support
- thin CLI dispatch if consistent with repo style
- focused tests
- queue evidence

Use the accepted Reference ID Scheme. EventRecord should refer to subjects, causation, correlation, evidence, reports, and future objects using stable `aide://...` refs where practical.

Minimum event families:
- WorkUnitStateChanged
- WorkerRunRecorded
- TestJobRecorded
- EvidencePacketRecorded
- AcceptanceRecorded
- CapabilityDeclared
- ConformanceResultRecorded
- ReferenceIDProjectionRecorded
- OKFProjectionRecorded
- ReconcilerFindingRecorded
- PatchTransactionRecorded

Important:
Defining event family names does not implement those systems.

Non-goals:
- no event sourcing runtime
- no append-only runtime event store
- no scheduler
- no leases
- no supervisor
- no Reconciler
- no OKF knowledge bundle
- no CapabilityManifest implementation
- no ConformanceProfile implementation
- no PatchTransaction implementation
- no AdapterManifest implementation
- no ContextPack v2
- no runtime reference registry
- no resolver service
- no database state
- no Service
- no Commander
- no provider adapters
- no Test Broker runtime
- no worker execution
- no branch/worktree automation
- no target apply
- no active apply
- no rollback execution
- no release
- no GitHub mutation
- no Gateway/network/model/provider calls
- no production readiness
- no release readiness
- no broad autonomous runtime behavior

Expected next task:
AIDE-CHECK-EVENT-RECORD-SCHEMA-01.
