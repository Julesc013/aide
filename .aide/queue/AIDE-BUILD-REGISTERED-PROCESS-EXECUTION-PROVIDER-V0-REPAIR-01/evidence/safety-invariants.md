# Safety Invariants

- Invalid specs launch zero processes.
- Missing executables launch zero processes.
- Digest mismatches launch zero processes.
- Failed preconditions launch zero processes.
- Mismatched bindings launch zero processes.
- Valid invocations launch at most once.
- Receipts describe the current invocation, not cumulative provider state.
- `shell` remains `false`.
- Raw environment values are not copied into launch metadata.
- State-probe failure fails closed.
- Decoder failure does not imply validation/evidence completeness.
- Process cancellation is unsupported in v0.
