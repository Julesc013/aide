# Prompt: AIDE-OPERATIONAL-HEALTH-PAUSE-01

Create and process `AIDE-OPERATIONAL-HEALTH-PAUSE-01` as a report-only
operational-health pause after
`AIDE-ACCEPT-CONFORMANCE-RESULT-SCHEMA-01`.

Use `.aide/queue/index.yaml` as canonical queue truth and re-read live
repository state before writing. Do not rely on chat history or stale generated
task packets.

Assess:

- live queue state and next-task ambiguity;
- accepted protocol/evidence baseline;
- ConformanceResult acceptance, repair, repair-check, and digest integrity;
- generated report/evidence volume, warning debt, OKF, Reconciler, ReportIndex,
  GeneratedOutputLedger, Track B B1, worktree, branch, and validation status;
- readiness for `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01`;
- explicit non-capabilities that must remain true.

Do not implement PatchTransaction or any later runtime, adapter, workbench,
provider, branch/worktree, target-apply, release, promotion, or mutation work.

Stop at `needs_review`. If healthy, recommend exactly:

```text
AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01
```
