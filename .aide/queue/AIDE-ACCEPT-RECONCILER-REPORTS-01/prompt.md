# Prompt: AIDE-ACCEPT-RECONCILER-REPORTS-01

Run a check-only acceptance review for `AIDE-BUILD-RECONCILER-REPORTS-01` and `AIDE-CHECK-RECONCILER-REPORTS-01`.

Accept only the narrow `minimal_reconciler_reports` capability if live evidence supports it:

- report-only Reconciler helper
- reconciler status/report/validate CLI dispatch
- finding taxonomy
- deterministic findings report
- queue/protocol/evidence/report/ReferenceID/EventRecord/OKF drift checks
- stale latest-task-packet detection/classification
- acceptance gate debt detection/classification
- missing evidence/report ref checks
- OKF/protocol/report mismatch checks
- capability overclaim checks
- ReferenceID/EventRecord report consumption
- advisory findings with mutation performed false
- no-repair/no-mutation boundary

Expected result if evidence remains coherent: `ACCEPTED_WITH_WARNINGS`.

Recommended next task if accepted: `AIDE-BUILD-CAPABILITY-MANIFEST-01`.

Do not repair Reconciler output, mutate source truth, refresh OKF, update latest-task-packet, rewrite protocol/reference/event records, implement CapabilityManifest, implement ConformanceProfile, implement PatchTransaction, implement AdapterManifest, implement ContextPack v2, implement runtime/service/provider/network/GitHub/branch/apply/release behavior, or claim production/release readiness.
