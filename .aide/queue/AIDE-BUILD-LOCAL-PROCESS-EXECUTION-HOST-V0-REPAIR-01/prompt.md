# Prompt

Create and process `AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-01`.

Repair exactly the six material findings from `AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-01`:

- disposable workspace not proven;
- path traversal, symlink, and reparse escape rejection not proven;
- raw NDJSON event stream and fail-closed event handling not proven;
- content-addressed worker artifacts not proven;
- WorkerRun lifecycle not proven;
- host descriptor overclaims operations.

Do not modify `RegisteredProcessExecutionProvider v0`, accepted ExecutionHost contract records, interop domains, hosts, `.aide.local`, provider/model/network surfaces, Workbench, Service, preview/apply/rollback, branch/worktree, GitHub, release, or promotion behavior.

Stop at `needs_review` with `PASS_WITH_WARNINGS`, proposed capability `local_process_execution_host_fixture_v0`, and recommend exactly `AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-01`.
