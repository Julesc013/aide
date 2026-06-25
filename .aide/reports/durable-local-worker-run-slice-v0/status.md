# Durable Local WorkerRun Slice v0

- status: PASS_WITH_WARNINGS
- proposed_capability_label: durable_local_worker_run_slice_v0
- authorization_result: allowed
- process_call_count: 1
- service_event_sequences: [1, 2, 3, 4, 5, 6]
- idempotent_replay_no_second_host_launch: true
- source_snapshot_unchanged: true
- recommended_next_task: AIDE-CHECK-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01

## Boundary

- Fixture-backed local WorkerRun recording only.
- Uses temporary local Service state by default.
- Does not implement a general worker harness, scheduler, Workbench runtime, preview, apply, rollback, network, provider/model, or repository mutation behavior.
