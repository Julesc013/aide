# AIDE-BUILD-RECONCILER-REPORTS-01 Prompt

Build the first report-only Reconciler slice after OKF acceptance.

The Reconciler should detect and report drift only. It must not repair drift, mutate source truth, rewrite generated context, refresh OKF pages, accept or supersede queue tasks, implement CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, runtime services, providers, Gateway, GitHub, network calls, branch/worktree automation, target apply, active apply, release, or promotion.

Required output includes `core/reconciler/reconciler_reports.py`, thin `reconciler status/report/validate` CLI dispatch, focused tests, `.aide/reports/reconciler/**`, queue evidence, and a stop at `needs_review`.

The expected next task after successful build is `AIDE-CHECK-RECONCILER-REPORTS-01`.
