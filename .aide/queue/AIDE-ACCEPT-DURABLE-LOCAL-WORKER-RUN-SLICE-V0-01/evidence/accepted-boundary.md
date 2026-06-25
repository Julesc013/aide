# Accepted Boundary

## Accepted

- `durable_local_worker_run_slice_v0`
- temporary local Service state for fixture-backed durable WorkerRun recording
- accepted local trust enforcement before launch
- accepted LocalProcessExecutionHost fixture behavior as the only launch path
- deterministic EventRecord and EvidencePacket projection
- idempotent replay without a second host run

## Not Accepted

- general worker harness
- autonomous AI worker
- remote ExecutionHost
- scheduler
- leases
- persistent background Service daemon
- Workbench runtime
- MCP runtime
- provider/model calls
- network calls
- PreviewSession
- DevelopmentTransaction
- preview/apply/rollback
- transaction approval
- source or target repository mutation
- branch/worktree automation
- GitHub mutation
- release or promotion
