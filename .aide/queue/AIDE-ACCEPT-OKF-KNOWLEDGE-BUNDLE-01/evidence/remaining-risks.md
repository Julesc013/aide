# Remaining Risks

- Full YAML parser integration is deferred; the accepted validation mode is the deterministic stdlib structural subset.
- `.aide/context/latest-task-packet.md` remains stale relative to `.aide/queue/index.yaml`.
- OKF pages can become stale if source queue, protocol, evidence, ReferenceID, or EventRecord records change without reprojection.
- Reconciler Reports is not implemented yet; drift detection remains future work.
- CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, and ContextPack v2 remain planned future slices.
- Runtime, Service, Commander, providers, Gateway, target apply, branch/worktree automation, release, GitHub mutation, and model/provider/network behavior remain deferred.

No remaining risk blocks acceptance of `minimal_okf_knowledge_bundle`.
