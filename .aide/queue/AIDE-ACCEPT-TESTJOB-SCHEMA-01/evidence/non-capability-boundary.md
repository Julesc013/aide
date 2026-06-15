# Non-Capability Boundary

Acceptance of `minimal_test_job_schema` does not authorize:

- Test Broker runtime
- async test execution
- test job submission
- test job run
- test job retry runtime
- test job summarize runtime
- worker execution
- WorkUnit claim
- WorkUnit run
- WorkUnit finish
- WorkUnit repair
- leases
- scheduler
- supervisor
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

The accepted capability is limited to metadata-only TestJob schema/helper/projection/validation and `test-job status/project/validate` CLI dispatch.
