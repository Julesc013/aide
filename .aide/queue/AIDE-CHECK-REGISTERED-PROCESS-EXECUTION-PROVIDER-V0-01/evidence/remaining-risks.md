# Remaining Risks

Material repair risks before provider acceptance or additional adapter proof:

- Binding/provider/capability mismatch can launch a process instead of failing
  closed before launch.
- Provider reuse can produce cumulative launcher counts and stale launch
  metadata in receipts.
- Decoder exceptions are represented but still report complete validation and
  evidence axes.
- State-probe failures are represented in receipts but can still report a
  complete typed result.
- Cancellation is neither implemented nor declared as an explicit
  non-capability.

These findings require a bounded repair task and independent recheck before
`registered_process_execution_provider_v0` can be used as an accepted substrate.
