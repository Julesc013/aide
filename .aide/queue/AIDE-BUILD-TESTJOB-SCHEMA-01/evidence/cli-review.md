# CLI Review

Status: PASS.

`.aide/scripts/aide_lite.py` now has thin dispatch for:

- `test-job status`
- `test-job project --source accepted-artifacts`
- `test-job validate`

Dispatch loads `core/protocol/test_job.py` and calls helper/report functions. Substantial protocol logic remains outside AIDE Lite.

Unsupported runtime-like subcommands are absent and fail closed through parser rejection, including:

- `test-job submit`
- `test-job run`
- `test-job retry`
- `test-job summarize`

No Test Broker, async execution, scheduler, lease, provider, network, Gateway, GitHub, or model behavior was added.
