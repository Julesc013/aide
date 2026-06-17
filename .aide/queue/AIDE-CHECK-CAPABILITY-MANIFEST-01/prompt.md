# AIDE-CHECK-CAPABILITY-MANIFEST-01

Independently check `AIDE-BUILD-CAPABILITY-MANIFEST-01`.

Use `.aide/queue/index.yaml` as canonical queue truth. Do not trust stale
context packets when they conflict with queue state.

Scope:

- Check only.
- Review the minimal declaration-only CapabilityManifest schema/helper/reports,
  CLI dispatch, tests, evidence, and source refs.
- Generate check evidence and reports only.
- Stop at `needs_review`.

Forbidden:

- No CapabilityManifest implementation repair.
- No ConformanceProfile or ConformanceResult.
- No conformance admission, adapter admission, adapter execution, or capability
  execution.
- No runtime registry, scheduler, leases, supervisor, Service, Commander,
  PatchTransaction, AdapterManifest, ContextPack v2, provider/model calls,
  network/Gateway/GitHub mutation, branch/worktree automation, target apply,
  active apply, release, production readiness, or broad autonomous runtime.

Expected result if live evidence matches the build claim:

```text
PASS_WITH_WARNINGS
```

Recommended next task if PASS or PASS_WITH_WARNINGS:

```text
AIDE-ACCEPT-CAPABILITY-MANIFEST-01
```

Do not recommend ConformanceProfile directly from this check.
