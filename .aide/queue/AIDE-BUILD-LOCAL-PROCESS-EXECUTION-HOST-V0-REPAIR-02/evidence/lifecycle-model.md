# WorkerRun Lifecycle Model

Explicit states:

- `proposed`
- `creating`
- `ready`
- `running`
- `completing`
- `completed`
- `failed`
- `timed_out`
- `cancelled`
- `reconciliation_required`

Terminal states:

- `completed`
- `failed`
- `timed_out`
- `cancelled`

The model accepts observed `run_cancelled` as a terminal outcome but keeps
public process cancellation unsupported. `reconciliation_required` is modeled as
a non-success boundary state, not as a completed run.

Focused tests cover creating-to-ready, ready-to-running, running-to-timed-out,
running-to-cancelled, running-to-reconciliation-required, invalid transition,
and terminal-state transition cases.
