# Next Task Prompt

```text
AIDE-ACCEPT-EVENT-RECORD-SCHEMA-01
```

Run this as a separate acceptance review gate. It should accept or reject only the checked `minimal_event_record_schema` capability after reviewing `AIDE-BUILD-EVENT-RECORD-SCHEMA-01` and `AIDE-CHECK-EVENT-RECORD-SCHEMA-01`.

Do not implement OKF, Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, event sourcing runtime, runtime event store, replay, provider behavior, branch/worktree automation, target apply, release behavior, GitHub mutation, Gateway calls, network calls, or model/provider calls in the acceptance gate.
