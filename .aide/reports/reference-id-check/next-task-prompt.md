# AIDE-ACCEPT-REFERENCE-ID-SCHEME-01
# Acceptance Review For Stable AIDE Reference ID Scheme

Create and process `AIDE-ACCEPT-REFERENCE-ID-SCHEME-01`.

Perform a check-only acceptance review over `AIDE-BUILD-REFERENCE-ID-SCHEME-01` and `AIDE-CHECK-REFERENCE-ID-SCHEME-01`.

Accept, accept-with-warnings, reject, or request hardening for only the minimal stable AIDE Reference ID Scheme capability.

Accepted capability target:

```text
minimal_reference_id_scheme
```

Acceptance scope:

- `aide://<kind>/<id>` stable identity syntax.
- ReferenceID schema/helper/projection/validation.
- `reference-id status/project/validate` CLI dispatch.
- Deterministic reference-map reports.
- File paths as locators, not identity.
- Optional SHA-256 locator metadata.
- Explicit required-vs-optional unknown-kind behavior.
- Predecessor compatibility with Envelope, EvidencePacket, WorkUnit, WorkerRun, and TestJob.

Non-goals:

- no EventRecord
- no OKF knowledge bundle
- no Reconciler
- no CapabilityManifest
- no ConformanceProfile
- no PatchTransaction
- no AdapterManifest
- no ContextPack v2
- no runtime reference registry
- no resolver service
- no database state
- no leases, scheduler, supervisor, Test Broker runtime, worker execution, Service, Commander, provider adapters, branch/worktree automation, target apply, active apply, rollback, release, Gateway, network, GitHub mutation, model/provider calls, production readiness, release readiness, or broad autonomous runtime behavior

Recommended next task if accepted:

```text
AIDE-BUILD-EVENT-RECORD-SCHEMA-01
```
