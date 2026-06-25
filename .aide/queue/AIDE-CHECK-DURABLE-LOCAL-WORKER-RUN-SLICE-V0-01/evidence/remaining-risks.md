# Remaining Risks

- The EventRecord payload drops the observed host result: `spec.payload.result`
  is `null` while the fixture report records `host_result: PASS`.
- `durable_local_worker_run_slice_v0` remains unaccepted until a bounded repair
  and independent repair check close this finding.
- Broader worker runtime capabilities remain non-capabilities: no general
  worker harness, autonomous AI worker, remote ExecutionHost, scheduler, leases,
  persistent daemon, Workbench/MCP runtime, provider/model calls, network calls,
  preview/apply/rollback, transaction approval, repository mutation, GitHub
  mutation, release, or promotion.
