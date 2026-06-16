# Prompt: AIDE-ACCEPT-REFERENCE-ID-SCHEME-01

Perform a check-only acceptance review over the stable AIDE Reference ID Scheme chain:

- `AIDE-BUILD-REFERENCE-ID-SCHEME-01`
- `AIDE-CHECK-REFERENCE-ID-SCHEME-01`

Accept or reject only the `minimal_reference_id_scheme` capability. Do not change ReferenceID behavior and do not implement EventRecord, OKF, Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, runtime registry, resolver service, database state, leases, scheduler, supervisor, Test Broker runtime, async execution, worker execution, Service, Commander, providers, branch/worktree behavior, target or active apply, rollback, uninstall, release, GitHub mutation, Gateway, network, model/provider calls, production readiness, release readiness, or broad runtime behavior.

Expected result if live evidence matches the build/check reports:

```text
ACCEPTED_WITH_WARNINGS
```

Accepted capability:

```text
minimal_reference_id_scheme
```

Recommended next task if accepted:

```text
AIDE-BUILD-EVENT-RECORD-SCHEMA-01
```
