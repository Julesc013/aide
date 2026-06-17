# Reconciler Acceptance Warning Disposition

All warnings are non-blocking for `minimal_reconciler_reports`.

| Warning | Blocking | Disposition |
| --- | --- | --- |
| Reconciler is report-only and does not repair drift. | false | accepted_with_warning |
| Findings are advisory and do not mutate queue/protocol/evidence/OKF truth. | false | accepted_with_warning |
| Stale latest-task-packet drift remains open. | false | accepted_with_warning |
| Acceptance gate debt remains open. | false | accepted_with_warning |
| Stale OKF build report routing remains open. | false | accepted_with_warning |
| OKF source-hash gaps remain open. | false | accepted_with_warning |
| Live finding schema differs from prompt field wording. | false | accepted_with_warning |
| CapabilityManifest is not implemented. | false | deferred to `AIDE-BUILD-CAPABILITY-MANIFEST-01` |
| ConformanceProfile, PatchTransaction, AdapterManifest, and ContextPack v2 are not implemented. | false | deferred to future queue tasks |
