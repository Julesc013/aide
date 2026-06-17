# AIDE-BUILD-RECONCILER-REPORTS-01
# Report-Only AIDE Reconciler

Create and process `AIDE-BUILD-RECONCILER-REPORTS-01`.

Use `.aide/queue/index.yaml` as canonical queue truth.

Goal:

Implement the first report-only Reconciler slice for AIDE.

This is a deterministic drift-detection/reporting slice, not a scheduler, repair engine, runtime, or mutator.

Build only:

- Reconciler report helper
- deterministic drift checks
- thin CLI dispatch if consistent with repo style
- reports
- focused tests
- queue evidence

The Reconciler must detect and report, not repair.

Initial report-only checks:

- stale `latest-task-packet.md` relative to queue truth
- acceptance gate debt
- contradictory queue statuses
- missing evidence refs
- missing report refs
- protocol/report/OKF mismatch
- capability overclaiming
- unsupported accepted-state claims
- stale generated reports
- missing source hashes where expected
- OKF/protocol/report mismatch
- `needs_review` items represented as accepted
- accepted capability pages without evidence refs
- EventRecord projection-only status mismatch
- ReferenceID locator/hash mismatch where reports expose it

Use accepted ReferenceID, EventRecord, and OKF knowledge where practical.

Non-goals:

- no repair
- no mutation
- no scheduler
- no leases
- no supervisor
- no runtime
- no Service
- no Commander
- no CapabilityManifest implementation
- no ConformanceProfile implementation
- no PatchTransaction implementation
- no AdapterManifest implementation
- no ContextPack v2
- no event sourcing runtime
- no append-only runtime store
- no target apply
- no active apply
- no branch/worktree automation
- no provider/model calls
- no network
- no Gateway/GitHub mutation
- no release
- no production readiness
- no broad autonomous runtime behavior

Expected commands:

```bat
py -3 .aide/scripts/aide_lite.py reconciler status
py -3 .aide/scripts/aide_lite.py reconciler report
py -3 .aide/scripts/aide_lite.py reconciler validate
```

Expected reports:

- `.aide/reports/reconciler/status.md`
- `.aide/reports/reconciler/reconciliation-report.json`
- `.aide/reports/reconciler/reconciliation-report.md`
- `.aide/reports/reconciler/validation.json`
- `.aide/reports/reconciler/validation.md`
- `.aide/reports/reconciler/findings.json`
- `.aide/reports/reconciler/findings.md`

Stop at `needs_review` with evidence.

Recommended next task:

```text
AIDE-CHECK-RECONCILER-REPORTS-01
```
