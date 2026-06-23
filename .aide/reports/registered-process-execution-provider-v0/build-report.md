# Registered Process Execution Provider v0 Build

Result: `PASS_WITH_WARNINGS`

Proposed capability:

```text
registered_process_execution_provider_v0
```

The provider is not accepted by this task. It is ready for independent check.

Generic components:

- `core/protocol/process_invocation.py`
- `core/protocol/execution_receipt.py`
- `core/execution/provider.py`
- `core/execution/registered_process.py`

Dominium adapter parity was preserved through focused fake-runner tests and
existing report validation. The live Dominium command was not rerun.
