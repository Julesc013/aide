# Next Task Prompt

```text
AIDE-ACCEPT-OKF-KNOWLEDGE-BUNDLE-01
```

This should be a check-only acceptance gate for `AIDE-BUILD-OKF-KNOWLEDGE-BUNDLE-01` and `AIDE-CHECK-OKF-KNOWLEDGE-BUNDLE-01`.

Accept only the bounded `minimal_okf_knowledge_bundle` capability if the acceptance review agrees with the build and check evidence.

Do not repair implementation files.

Do not implement Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, Runtime, Service, Commander, providers, Gateway, target apply, branch/worktree automation, release, GitHub mutation, or provider/model/network behavior.

If accepted, record the explicit non-capability boundary and only then select the next queue item.
