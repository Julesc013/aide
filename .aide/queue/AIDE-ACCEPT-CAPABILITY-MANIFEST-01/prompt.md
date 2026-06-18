# AIDE-ACCEPT-CAPABILITY-MANIFEST-01

Run a check-only acceptance review for `AIDE-BUILD-CAPABILITY-MANIFEST-01` and
`AIDE-CHECK-CAPABILITY-MANIFEST-01`.

Accept only the narrow `minimal_capability_manifest` capability if live evidence
supports it:

- CapabilityManifest schema
- CapabilityManifest helper/projection/validation
- `capability-manifest status`, `capability-manifest project`, and
  `capability-manifest validate` CLI dispatch
- deterministic 11-capability inventory
- accepted capability state projection
- accepted_with_warnings preservation
- metadata_only/report_only/projection_only/runtime/mutating status semantics
- evidence/source/report/event/OKF refs
- Reconciler warning integration where practical
- explicit non-capability preservation
- conformance placeholder boundary

Expected result if evidence remains coherent: `ACCEPTED_WITH_WARNINGS`.

Recommended next task if accepted: `AIDE-BUILD-CONFORMANCE-PROFILE-01`.

Generate the first prompt batch:

```text
AIDE-ACCEPT-CAPABILITY-MANIFEST-01
AIDE-BUILD-CONFORMANCE-PROFILE-01
AIDE-CHECK-CONFORMANCE-PROFILE-01
```

Execute only `AIDE-ACCEPT-CAPABILITY-MANIFEST-01` in this task.

Do not implement ConformanceProfile, ConformanceResult, conformance admission,
adapter admission, adapter execution, capability execution, runtime capability
registry, scheduler, leases, supervisor, runtime, Service, Commander,
PatchTransaction, AdapterManifest, ContextPack v2, event sourcing runtime,
append-only runtime store, Test Broker runtime, async execution, worker
execution, target apply, active apply, branch/worktree automation,
provider/model calls, network, Gateway/GitHub mutation, release, production
readiness, or broad autonomous runtime behavior.
