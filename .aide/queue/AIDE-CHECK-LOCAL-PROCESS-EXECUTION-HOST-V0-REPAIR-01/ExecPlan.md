# AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-01 ExecPlan

## Objective

Check only: independently verify Repair 01 closure of the six material findings from `AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-01`.

## Scope

Allowed edits are limited to this check task packet, check reports under `.aide/reports/local-process-execution-host-repair-01-check/`, `.aide/queue/index.yaml`, `PLANS.md`, and `IMPLEMENT.md`.

Production implementation, fixtures, tests, provider core, accepted ExecutionHost contract, source repair reports, and `.aide.local` state are read-only for this check.

## Method

1. Verify source chain, clean state, source task result, and exact six source findings.
2. Inspect the latest repair diff for forbidden-path changes.
3. Run an evidence-local check harness that inspects source text, generated reports, and public production behavior as system-under-test.
4. Re-run focused and regression validation without modifying implementation.
5. Record material findings and stop at `needs_review`.

## Exit Criteria

If no material findings remain, record `PASS_WITH_WARNINGS` and recommend `AIDE-ACCEPT-LOCAL-PROCESS-EXECUTION-HOST-V0-01`.

If any material finding remains, record `REQUEST_CHANGES` and recommend `AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-02`.
