# Remaining Risks

- Full JSON Schema Draft 2020-12 validation remains deferred; local minimal schema validation passed.
- ReferenceID does not resolve references at runtime.
- EventRecord is not implemented by this acceptance; it is only the recommended next build task.
- OKF, Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, and runtime coordination remain future work.
- `.aide/context/latest-task-packet.md` remains stale relative to live queue truth.

Mitigation:

- Preserve all listed limitations as explicit non-capabilities.
- Route exactly one next task: `AIDE-BUILD-EVENT-RECORD-SCHEMA-01`.
- Do not implement runtime, resolver, OKF, patch, adapter, service, provider, branch/worktree, target-apply, active-apply, release, Gateway, network, GitHub, or model/provider behavior without a future reviewed queue item.
