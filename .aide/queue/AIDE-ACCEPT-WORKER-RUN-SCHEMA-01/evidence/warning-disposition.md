# Warning Disposition

## Full Draft 2020-12 JSON Schema validation remains deferred

- Blocking: false.
- Reason: the accepted predecessor pattern uses the local minimal JSON Schema subset, and WorkerRun helper/schema alignment passes.
- Mitigation: defer full schema engine or conformance hardening to a later reviewed protocol/conformance task.

## WorkerRun remains metadata-only by design

- Blocking: false.
- Reason: metadata-only WorkerRun records are the accepted scope of `minimal_worker_run_schema`.
- Mitigation: do not implement execution until TestJob, claim/lease, provider, and runtime boundaries have their own accepted tasks.

## latest-task-packet.md is stale relative to queue truth

- Blocking: false.
- Reason: live `.aide/queue/index.yaml` and task-local packets are canonical for this review.
- Mitigation: leave packet repair to a separate authorized hygiene task.

## Prior check harness probes were corrected by reruns

- Blocking: false.
- Reason: the check report records corrected reruns with PASS outcomes.
- Mitigation: use the corrected direct command forms in future acceptance/check tasks.

## Generated report churn must be contained

- Blocking: false.
- Reason: check evidence records out-of-scope report churn was restored.
- Mitigation: continue restoring generated churn unless the reports are deliberate task deliverables.
