# Remaining Risks

Non-blocking risks:

- CapabilityManifest is declaration-only and does not prove behavior.
- ConformanceProfile and ConformanceResult remain future work.
- Adapter admission and adapter execution remain future work.
- PatchTransaction, AdapterManifest, ContextPack v2, runtime registry,
  scheduler, leases, supervisor, Service, Commander, providers, network,
  Gateway, GitHub mutation, branch/worktree automation, target apply, active
  apply, release, and production readiness remain deferred.
- Stale latest-task-packet and OKF source-hash drift remain warning-class debt.
- Accepted predecessor capability warnings remain preserved rather than
  flattened to a clean pass.

Mitigation:

- Route next to `AIDE-BUILD-CONFORMANCE-PROFILE-01`.
- Treat CapabilityManifest as declaration, not admission.
- Keep future mutation safety behind PatchTransaction and conformance gates.
