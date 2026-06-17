# Remaining Risks

- Reconciler acceptance does not repair drift; it only admits report-only drift detection.
- Stale latest-task-packet drift remains open until a future authorized context refresh.
- Acceptance gate debt remains open until future review tasks process queued work.
- Stale OKF build report routing and OKF source-hash gaps remain open until a future authorized OKF refresh.
- CapabilityManifest is not implemented by this task; it is only selected as next work.
- ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, runtime, Service, Commander, provider adapters, branch/worktree automation, target apply, active apply, release, and promotion remain future work.

No blocker prevents routing to `AIDE-BUILD-CAPABILITY-MANIFEST-01`.
