# Remaining Risks

Non-blocking warnings:

- CapabilityManifest declares state but does not prove conformance.
- ConformanceProfile and ConformanceResult are not implemented.
- Adapter admission and adapter execution are not implemented.
- Runtime capability registry is not implemented.
- PatchTransaction, AdapterManifest, and ContextPack v2 are not implemented.
- Stale latest-task-packet drift remains reported and unresolved.
- OKF source-hash drift remains warning-class and unresolved.

Mitigation:

- Stop at review and route to `AIDE-CHECK-CAPABILITY-MANIFEST-01`.
