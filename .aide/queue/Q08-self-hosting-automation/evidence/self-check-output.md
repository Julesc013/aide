# Q08 Self-Check Output Evidence

`py -3 scripts/aide self-check --write-report` wrote:

- `.aide/runs/self-check/latest.md`

The report is deterministic for the current repository state and intentionally contains no timestamp.

Key anchors from the output:

```text
AIDE self-check
mode: report-only
mutation: none
canonical: false
external_calls: none
provider_or_model_calls: none
network_calls: none
automatic_worker_invocation: false
queue_auto_merge: false
```

Validation summary:

```text
validation:
- status: PASS_WITH_WARNINGS
- info: 148
- warning: 8
- error: 0
```

Generated artifact drift summary:

```text
generated_artifact_drift:
- manifest_source_fingerprint: stale
- handling: report-only; Q08 does not refresh generated artifacts
- manifest_operation_if_compile_write: would_replace (manifest)
- generated_artifacts_refreshed: false
```

Next-step summary:

```text
next_recommended_step: Q08 review according to .aide/queue/Q08-self-hosting-automation/status.yaml
```

The full latest report is stored at `.aide/runs/self-check/latest.md`.
