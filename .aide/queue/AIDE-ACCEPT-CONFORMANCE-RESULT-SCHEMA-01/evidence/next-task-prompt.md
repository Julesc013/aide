# AIDE-OPERATIONAL-HEALTH-PAUSE-01
# Report-Only Operational Health Pause Before Mutation Work

Create and process `AIDE-OPERATIONAL-HEALTH-PAUSE-01`.

Use `.aide/queue/index.yaml` as canonical queue truth.

Scope:

- report-only operational-health pause
- no implementation
- no schema/helper/test changes
- no PatchTransaction
- no adapter work
- no runtime work
- no branch mutation
- no target mutation
- no provider/model/network calls

Review:

- queue status and next authorized work;
- accepted protocol/evidence capabilities through ConformanceResult;
- historical failed-check preservation;
- generated report and evidence overhead;
- open warning debt;
- OKF/reconciler freshness;
- worktree and branch state;
- explicit non-capabilities.

Output:

- task-local evidence;
- a concise health report;
- recommended serialized next task after the pause.

Do not begin PatchTransaction until this pause is complete.
