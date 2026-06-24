# Warning Disposition

Accepted warnings for this build:

- ExecutionHost contract v0 is projection-only.
- Worker/session execution remains separate from deterministic capability execution.
- LocalProcessExecutionHost is intentionally deferred until after independent check and acceptance.
- Full JSON Schema Draft 2020-12 validation remains future work; the local helper uses the existing minimal schema subset.

These warnings are non-blocking because the task explicitly forbids live host
execution and requires a projection-only contract.
