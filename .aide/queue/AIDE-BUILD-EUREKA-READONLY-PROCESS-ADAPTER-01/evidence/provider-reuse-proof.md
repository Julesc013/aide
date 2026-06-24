# Provider Reuse Proof

The adapter uses `RegisteredProcessExecutionProvider v0` through the shared:

- `RegisteredProcessSpec`;
- `CapabilityInvocation`;
- `CapabilityBinding`;
- `ProcessExecutionReceipt`;
- `CapabilityOutcome`;
- precondition, state-probe, decoder, runner, and scrubber seams.

The task did not modify provider core or neutral protocol files.
