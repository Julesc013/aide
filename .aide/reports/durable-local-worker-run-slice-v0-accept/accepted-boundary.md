# Accepted Boundary

Accepted:

```text
durable_local_worker_run_slice_v0
```

This means AIDE can durably record one bounded fixture-backed local WorkerRun
using already accepted local Service, local trust enforcement,
RegisteredProcessExecutionProvider v0, and LocalProcessExecutionHost fixture
behavior.

This acceptance is deliberately narrower than a runtime product. It does not
accept general worker execution, autonomous AI workers, a scheduler, leases,
persistent daemon behavior, Workbench/MCP runtime, network/provider/model calls,
preview/apply/rollback, transaction approval, repository mutation, GitHub
mutation, release, or promotion.
