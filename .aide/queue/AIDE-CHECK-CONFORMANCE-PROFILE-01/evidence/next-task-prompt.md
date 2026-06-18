# Next Task Prompt

Run `AIDE-ACCEPT-CONFORMANCE-PROFILE-01`.

Consolidate:

- `AIDE-BUILD-CONFORMANCE-PROFILE-01`
- `AIDE-CHECK-CONFORMANCE-PROFILE-01`
- profile_ref `aide://conformance-profile/minimal_capability_manifest-v1.0.0`
- subject_ref `aide://capability/minimal_capability_manifest`

Expected acceptance posture:

```text
ACCEPTED_WITH_WARNINGS
```

Required boundary: acceptance must not implement ConformanceResult, conformance
execution, conformance admission, adapter admission/execution, PatchTransaction,
AdapterManifest, ContextPack v2, runtime, provider/model/network calls, target
apply, branch/worktree automation, release, promotion, or production readiness.
