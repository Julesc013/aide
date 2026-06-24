# Binding Safety Review

- result: `FAIL`
- capability_mismatch_calls: `1`
- wrong_provider_calls: `1`

Finding: mismatched capability/provider bindings launch a process and must fail closed before launch.
