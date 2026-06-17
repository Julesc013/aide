# AIDE-BUILD-CAPABILITY-MANIFEST-01

Build the minimal AIDE CapabilityManifest protocol slice.

Use `.aide/queue/index.yaml` as canonical queue truth. Treat stale generated
context packets and attached prompt history as non-authoritative when they
conflict with the filesystem queue.

Scope:

- CapabilityManifest schema, helper, projection, validation, reports, thin CLI,
  focused tests, queue evidence, and next-task prompt only.
- Declaration-only; CapabilityManifest declares capability state and preserves
  status semantics, but does not prove conformance or admit execution.
- Project the accepted AIDE chain through `minimal_reconciler_reports`.

Forbidden:

- No ConformanceProfile, ConformanceResult, admission, adapter execution,
  capability execution, runtime registry, scheduler, leases, supervisor,
  Service, Commander, PatchTransaction, AdapterManifest, ContextPack v2,
  provider/model calls, network/Gateway/GitHub mutation, branch/worktree
  automation, target apply, active apply, release, production readiness, or
  broad autonomous runtime.

Expected result: `PASS_WITH_WARNINGS`, stopping at `needs_review`.

Recommended next task if implementation passes or passes with warnings:

```text
AIDE-CHECK-CAPABILITY-MANIFEST-01
```
