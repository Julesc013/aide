# Lifecycle Validation

WorkerRun lifecycle is computed from the raw event sequence.

The valid live sequence is:

```text
proposed
→ creating
→ ready
→ running
→ completing
→ completed
```

Invalid ordering and terminal-state transitions are refused by the lifecycle validator.

The generated lifecycle projection is `.aide/reports/local-process-execution-host/worker-run.json`.
