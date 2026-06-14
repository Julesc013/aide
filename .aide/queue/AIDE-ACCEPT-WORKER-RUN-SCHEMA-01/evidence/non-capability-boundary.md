# Non-Capability Boundary

Acceptance of `minimal_worker_run_schema` does not authorize:

- worker execution
- WorkUnit claim
- WorkUnit run
- WorkUnit finish
- WorkUnit repair
- leases
- scheduler
- supervisor
- TestJob
- Test Broker
- Service
- Commander
- provider adapters
- branch/worktree automation
- target apply
- active apply
- rollback execution
- uninstall execution
- release
- promotion
- Gateway
- network
- GitHub mutation
- model/provider calls
- production readiness
- release readiness
- broad autonomous runtime

The accepted capability is limited to metadata-only WorkerRun schema/helper/projection/validation and worker-run status/project/validate CLI dispatch.
