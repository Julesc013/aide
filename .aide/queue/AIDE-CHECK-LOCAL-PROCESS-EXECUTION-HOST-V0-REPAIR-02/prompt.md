# Prompt

Create and process `AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-02`.

This is a check-only task. Do not repair implementation.

Independently verify that
`AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-02` closes the seven material
assertions from `AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-01`:

- `workspace.path_probe_matrix`
- `workspace.test_matrix_incomplete`
- `events.duplicate_terminal_reason`
- `events.test_matrix_incomplete`
- `artifacts.test_matrix_incomplete`
- `lifecycle.cancelled_terminal_missing`
- `lifecycle.test_matrix_incomplete`

Also verify that the already-closed disposable workspace and descriptor-scope
findings remain closed, no forbidden surfaces changed, and no new capabilities
are claimed.

If all material checks pass, recommend exactly
`AIDE-ACCEPT-LOCAL-PROCESS-EXECUTION-HOST-V0-01`.

If material findings remain, recommend exactly
`AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-03`.
