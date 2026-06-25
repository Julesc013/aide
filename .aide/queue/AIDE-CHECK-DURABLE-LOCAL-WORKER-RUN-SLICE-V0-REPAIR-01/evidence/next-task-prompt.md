# Next Task Prompt

Create and process:

```text
AIDE-ACCEPT-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01
```

Accept only `durable_local_worker_run_slice_v0` as a fixture-backed durable
local WorkerRun recording slice using accepted local Service, local trust
enforcement, RegisteredProcessExecutionProvider v0, and LocalProcessExecutionHost
fixture behavior.

Do not accept:

- general worker harness;
- autonomous AI worker;
- remote ExecutionHost;
- scheduler;
- leases;
- persistent background Service;
- Workbench runtime;
- MCP runtime;
- provider/model calls;
- network calls;
- preview/apply/rollback;
- transaction approval;
- repository mutation;
- branch/worktree automation;
- GitHub mutation;
- release or promotion.
