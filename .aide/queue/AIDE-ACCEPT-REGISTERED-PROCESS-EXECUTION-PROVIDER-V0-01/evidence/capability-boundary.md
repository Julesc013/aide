# Capability Boundary

Accepted:

- immutable registered process specs;
- binding and provider coherence checks;
- precondition checks;
- `shell=false` launch through the registered provider;
- one-launch accounting per invocation;
- bounded timeout and stream summaries;
- stream scrubbing;
- state-probe and decoder hooks;
- neutral `ProcessExecutionReceipt`;
- neutral `CapabilityOutcome`;
- fail-closed behavior for invalid specs, preconditions, timeouts, decoder failures, and state-probe failures.

Not accepted:

- arbitrary shell or command dispatch;
- worker sessions;
- ExecutionHost;
- Service/runtime/Workbench behavior;
- provider/model/network calls;
- preview/apply/rollback;
- repository, branch/worktree, GitHub, release, or promotion mutation.
