# Queue Drift Review

Status: `PASS_WITH_WARNINGS`

Live queue evidence:

- `AIDE-BUILD-RECONCILER-REPORTS-01` is present in `.aide/queue/index.yaml`.
- The build task status is `needs_review`.
- `task inspect --task-id AIDE-BUILD-RECONCILER-REPORTS-01` reported a complete task with no missing evidence.
- `task evidence --task-id AIDE-BUILD-RECONCILER-REPORTS-01` listed the expected build evidence files.

Drift observed by the Reconciler:

- Latest generated task packet points to `AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-01`.
- The queue has existing acceptance gate debt.

This check records those drift items as warnings only and does not rewrite generated context or task state.
