# AIDE-BUILD-AIDE-SELF-VALIDATION-PROCESS-ADAPTER-01

Create and process `AIDE-BUILD-AIDE-SELF-VALIDATION-PROCESS-ADAPTER-01`.

Repo truth outranks this prompt. Inspect
`AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01`, its source
repair and check chain, queue policy, queue index, `PLANS.md`, `IMPLEMENT.md`,
the registered-process provider implementation, focused provider tests, and
current AIDE validation commands.

Build the first reuse proof after the repaired provider check by adding a thin
AIDE self-validation process adapter over the same proposed
`RegisteredProcessExecutionProvider v0`.

The adapter should invoke the existing deterministic AIDE validation command
through an immutable registered process spec, exact argv vector, `shell=False`,
environment constraints, preflight, declared state-probe coverage, stream
scrubbing, receipt/outcome projection, and evidence. Prefer fake-runner and
fixture-backed tests. Do not accept the provider in this task.

Required result: `PASS` or `PASS_WITH_WARNINGS` at `needs_review`.

Recommended next task only:

```text
AIDE-CHECK-AIDE-SELF-VALIDATION-PROCESS-ADAPTER-01
```
