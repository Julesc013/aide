# Idempotency

The fixture records an idempotency row for the durable WorkerRun request. A
second replay of the same request returns the existing WorkerRun reference and
does not launch the accepted local host a second time.

Observed:

- `process_call_count: 1`
- `idempotency_status: recorded`
- `idempotent_replay_status: duplicate`
- `idempotent_replay_no_second_host_launch: true`
