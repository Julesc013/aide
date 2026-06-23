# Extracted Components

- `core/protocol/process_invocation.py`: `CapabilityInvocation`,
  `CapabilityBinding`, and typed `ArgumentToken` records.
- `core/protocol/execution_receipt.py`: neutral `CapabilityOutcome` and
  `ProcessExecutionReceipt` records plus stable digest helpers.
- `core/execution/provider.py`: execution provider protocol.
- `core/execution/registered_process.py`: registered-process provider,
  immutable spec, precondition, state-probe, decoder, scrubber, and fake-runner
  test seams.
- `core/interop/dominium/registered_validation_backend.py`: thin Dominium
  adapter over the generic provider.
