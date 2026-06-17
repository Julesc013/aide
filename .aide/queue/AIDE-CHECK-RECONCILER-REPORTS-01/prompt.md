# Prompt: AIDE-CHECK-RECONCILER-REPORTS-01

Run a check-only independent review of `AIDE-BUILD-RECONCILER-REPORTS-01`.

The check must not repair, rebuild, or mutate the Reconciler implementation or predecessor artifacts. It must review live queue truth, build evidence, generated Reconciler reports, report-only boundaries, CLI behavior, tests, predecessor compatibility, and overclaiming controls.

Expected result, if the live evidence matches the build task, is `PASS_WITH_WARNINGS`. Stop at `needs_review` and recommend `AIDE-ACCEPT-RECONCILER-REPORTS-01` next. Do not recommend CapabilityManifest directly from this check.

Required outputs:

- `.aide/queue/AIDE-CHECK-RECONCILER-REPORTS-01/task.yaml`
- `.aide/queue/AIDE-CHECK-RECONCILER-REPORTS-01/ExecPlan.md`
- `.aide/queue/AIDE-CHECK-RECONCILER-REPORTS-01/prompt.md`
- `.aide/queue/AIDE-CHECK-RECONCILER-REPORTS-01/status.yaml`
- `.aide/queue/AIDE-CHECK-RECONCILER-REPORTS-01/evidence/*.md`
- `.aide/reports/reconciler-check/check-report.json`
- `.aide/reports/reconciler-check/check-report.md`
- `.aide/reports/reconciler-check/status.md`
- `.aide/reports/reconciler-check/next-task-prompt.md`

Non-capabilities remain explicit: no drift repair, source truth mutation, queue acceptance mutation, latest-task-packet rewrite, OKF projection refresh, protocol report rewrite, ReferenceID or EventRecord rewrite, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, runtime Reconciler service, scheduler, leases, supervisor, Test Broker runtime, async execution, worker execution, Service, Commander, provider adapters, branch/worktree automation, target apply, active apply, rollback, uninstall, release, promotion, GitHub mutation, Gateway calls, network calls, provider/model calls, production readiness, release readiness, or broad autonomous runtime behavior.
