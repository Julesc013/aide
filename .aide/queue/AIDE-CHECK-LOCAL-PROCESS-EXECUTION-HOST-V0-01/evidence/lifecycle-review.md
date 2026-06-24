# Lifecycle Review

- REQUEST_CHANGES: legal WorkerRun lifecycle transitions are not validated.
- REQUEST_CHANGES: unsupported lifecycle operations are not tested as typed refusals.
- Timeout refusal is tested, but cancellation and reconciliation remain explicit non-capabilities.
