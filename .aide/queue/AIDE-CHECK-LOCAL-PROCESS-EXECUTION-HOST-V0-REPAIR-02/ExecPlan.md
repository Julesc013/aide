# AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-02 ExecPlan

## Objective

Check only: verify that Repair 02 closes the seven material assertions from the
Repair 01 check without modifying implementation or accepting the capability.

## Scope

Allowed edits are limited to this check task, check reports under
`.aide/reports/local-process-execution-host-repair-02-check/`, queue index
routing, and root logs.

Production implementation, focused tests, provider core, accepted contract,
fixtures, source repair reports, hosts, interop domains, and `.aide.local` are
read-only for this task.

## Method

1. Verify source chain and forbidden-path scope.
2. Exercise the production LocalProcessExecutionHost behavior as system under
   test through a task-local independent harness.
3. Re-run focused and regression validation.
4. Record material assertions and route to acceptance or Repair 03.

## Exit Criteria

If material findings remain, stop at `needs_review` with `REQUEST_CHANGES` and
recommend `AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-03`.

If no material findings remain, stop at `needs_review` with
`PASS_WITH_WARNINGS` and recommend
`AIDE-ACCEPT-LOCAL-PROCESS-EXECUTION-HOST-V0-01`.
