# Remaining Risks And Warnings

- The accepted slice is fixture-backed and local only.
- It uses temporary local Service state by default and does not create
  persistent `.aide.local` state.
- It records a bounded local WorkerRun fixture; it is not a general worker
  harness, autonomous AI worker runtime, scheduler, or remote ExecutionHost.
- It does not implement preview, apply, rollback, transaction approval, provider
  calls, network calls, Workbench/MCP runtime, GitHub mutation, release, or
  promotion behavior.
