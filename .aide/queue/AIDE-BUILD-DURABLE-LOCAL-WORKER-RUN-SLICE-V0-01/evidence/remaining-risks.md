# Remaining Risks

- The slice is fixture-backed and local only.
- The accepted LocalProcessExecutionHost fixture remains the only process launch path.
- No persistent daemon, scheduler, leases, cancellation, resource quota manager,
  provider/model call, network call, Workbench runtime, preview, apply, rollback,
  or repository mutation behavior is implemented.
- The durable state store is temporary by default; persistent `.aide.local`
  runtime state remains future work.
