# AIDE-CHECK-EUREKA-READONLY-PROCESS-ADAPTER-01 ExecPlan

## Objective

Independently check the Eureka read-only process adapter build at commit
`961add0` without repairing implementation or accepting the provider.

## Scope

Allowed changes are this check task packet, check reports, queue index routing,
and focused root log updates.

Implementation files, provider core, neutral protocol files, source build
reports, AIDE self-adapter, Dominium adapter, and the Eureka checkout are
read-only for this phase.

## Plan

1. Verify source build status, reports, and committed evidence.
2. Inspect provider/core immutability and genericity.
3. Inspect the selected Eureka command and external checkout state read-only.
4. Re-run report validation and focused regression tests without invoking
   Eureka again.
5. Scan committed build artifacts for local paths and secret-like values.
6. Write check report/evidence and stop at `needs_review`.

## Exit

`PASS_WITH_WARNINGS`, material finding count `0`, missing evidence `0`, provider
still proposed and unaccepted, and next task exactly
`AIDE-ACCEPT-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01`.
