# Prompt

Create and process `AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-02`.

Repo truth outranks this prompt.

Repair exactly the seven remaining material assertions from
`AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-01`:

- `workspace.path_probe_matrix`
- `workspace.test_matrix_incomplete`
- `events.duplicate_terminal_reason`
- `events.test_matrix_incomplete`
- `artifacts.test_matrix_incomplete`
- `lifecycle.cancelled_terminal_missing`
- `lifecycle.test_matrix_incomplete`

Preserve the two already-closed Repair 01 findings:

- `local_host.disposable_workspace_not_proven`
- `local_host.descriptor_overclaims_operations`

Do not redesign LocalProcessExecutionHost, broaden it beyond the deterministic
fixture-backed reference host, change `RegisteredProcessExecutionProvider v0`,
change the accepted ExecutionHost contract, implement Service, Workbench, MCP,
provider/model/network calls, arbitrary worker execution, preview, apply,
rollback, repository mutation, branch/worktree automation, GitHub mutation,
release, or promotion.

Stop at `needs_review` and recommend exactly
`AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-02`.
