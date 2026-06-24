# Remaining Risks And Deferrals

- Independent check is required before `local_process_execution_host_v0` can be accepted.
- This is a bounded local reference worker fixture, not a generic worker harness.
- Cancellation is not implemented.
- Durable idempotency is not implemented.
- Streaming artifact storage is not implemented.
- Resource quotas are not implemented.
- Worker leases are not implemented.
- Scheduler and supervisor behavior are not implemented.
- Service/runtime and Workbench behavior are not implemented.
- Provider/model calls and network calls remain forbidden and unimplemented.
- Preview/apply/rollback and repository mutation remain forbidden and unimplemented.
- Non-Windows platforms and minimum supported Python versions were not separately executed in this build task.
