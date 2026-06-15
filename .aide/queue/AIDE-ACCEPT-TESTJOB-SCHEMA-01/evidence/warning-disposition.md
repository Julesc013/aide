# Warning Disposition

## Full Draft 2020-12 JSON Schema validation remains deferred

- Blocking: false.
- Reason: the accepted predecessor pattern uses the local minimal JSON Schema subset, and TestJob helper/schema alignment passes.
- Mitigation: defer full schema engine or conformance hardening to a later reviewed protocol/conformance task.

## TestJob remains metadata-only by design

- Blocking: false.
- Reason: metadata-only TestJob records are the accepted scope of `minimal_test_job_schema`.
- Mitigation: do not implement Test Broker runtime or async execution until a future reviewed queue item authorizes it.

## Test Broker runtime and async execution are absent

- Blocking: false.
- Reason: absence is the required boundary for this protocol slice.
- Mitigation: preserve explicit non-capabilities and fail-closed unsupported subcommands.

## latest-task-packet.md is stale relative to queue truth

- Blocking: false.
- Reason: live `.aide/queue/index.yaml` and task-local packets are canonical for this review.
- Mitigation: leave packet repair to a separate authorized hygiene task.

## Prior check scan invocations were corrected by reruns

- Blocking: false.
- Reason: the check report records corrected reruns with PASS outcomes.
- Mitigation: use corrected direct command forms in future acceptance/check tasks.

## Generated report churn must be contained

- Blocking: false.
- Reason: check evidence records out-of-scope report churn was restored.
- Mitigation: continue restoring generated churn unless the reports are deliberate task deliverables.

## ReferenceID is the next task before PatchTransaction

- Blocking: false.
- Reason: the user-supplied frozen sequence places `AIDE-BUILD-REFERENCE-ID-SCHEME-01` after TestJob acceptance.
- Mitigation: recommend ReferenceID next unless a later reviewed queue item changes the sequence.
