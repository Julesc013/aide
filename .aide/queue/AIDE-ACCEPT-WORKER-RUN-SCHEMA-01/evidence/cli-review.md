# CLI Review

Status: PASS.

`.aide/scripts/aide_lite.py` has thin dispatch for:

- `worker-run status`
- `worker-run project --source accepted-artifacts`
- `worker-run validate`

Dispatch loads `core/protocol/worker_run.py` and calls helper/report functions. Unsupported execution-like WorkerRun subcommands such as `run`, `start`, `claim`, and `lease` are absent and fail closed through parser rejection.

No CLI implementation was changed by this acceptance review.
