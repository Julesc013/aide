# Remaining Risks

Non-blocking risks:

- CapabilityManifest is declaration-only and does not prove behavior.
- Acceptance is not granted by this check.
- ConformanceProfile and ConformanceResult remain future work.
- Adapter admission and adapter execution remain future work.
- PatchTransaction, AdapterManifest, ContextPack v2, runtime registry,
  scheduler, leases, supervisor, Service, Commander, providers, network,
  Gateway, GitHub mutation, branch/worktree automation, target apply, active
  apply, release, and production readiness remain deferred.
- Stale latest-task-packet and OKF source-hash drift remain warning-class.

Mitigation:

- Route next to `AIDE-ACCEPT-CAPABILITY-MANIFEST-01`.
- Do not recommend ConformanceProfile directly from this check.
