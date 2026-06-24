# Contract Boundary

This build defines projection-only records:

- `ExecutionHostDescriptor`
- `ExecutionHostRunBinding`
- `ExecutionHostEvent`
- `ExecutionHostArtifact`
- `ExecutionHostApproval`
- `ExecutionHostUsage`

It reserves the v0 operation vocabulary:

- `probe`
- `create_run`
- `attach`
- `send_input`
- `stream_events`
- `resolve_runtime_approval`
- `interrupt`
- `collect_artifacts`
- `finish`
- `reconcile`

The records explicitly keep `registered_process_execution_provider_v0` as the
deterministic capability-execution provider and do not collapse capability
execution into worker/session execution.
