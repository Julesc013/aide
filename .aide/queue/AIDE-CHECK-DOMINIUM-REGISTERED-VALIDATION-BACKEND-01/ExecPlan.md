# ExecPlan: AIDE-CHECK-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01

## Objective

Independently check `AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01`
without repairing it. The decisive question is whether the build proved a
Dominium-owned command boundary and whether its proposed capability label is
precise enough for acceptance.

## Scope

Allowed changes are limited to this check task packet, task-local evidence, the
check report directory, `.aide/queue/index.yaml`, `PLANS.md`, and
`IMPLEMENT.md`.

The check may read the AIDE repository, the build reports, and the pinned local
Dominium checkout. It may run read-only Git state probes and AIDE validation
commands. It must not invoke the live Dominium CLI again, repair production
code, mutate Dominium, broaden dispatch, call providers/models/network, run
workers, start Workbench or Service behavior, preview/apply/rollback, or invoke
GitHub/release behavior.

## Plan

1. Confirm the build task and reports are present, complete, and still routed
   to this check.
2. Inspect the backend source and build evidence for actual process-entry,
   output-origin, false-boundary, and no-fixture claims.
3. Inspect the pinned Dominium CLI, command, and service adapter source to
   corroborate the refusal path independently from AIDE booleans.
4. Recompute read-only Dominium revision, clean status, tracked-tree digest,
   and command implementation digests.
5. Scan generated build/check reports for local absolute paths and secret-like
   values.
6. Decide whether the proposed capability label overclaims the observed
   boundary and select exactly one next task.
7. Run validation, write evidence, restore unrelated generated churn, and stop
   at `needs_review`.

## Progress

- [x] Baseline queue policy reviewed.
- [x] Source build task and reports inspected.
- [x] Dominium command/refusal path inspected.
- [x] Independent harness written and executed.
- [x] Reports and evidence written.
- [x] Validation completed.
- [x] Stopped at `needs_review`.

## Exit

If no material truthfulness or safety findings remain, recommend
`AIDE-ACCEPT-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01`.

Result is `REQUEST_CHANGES`. The command-boundary mechanics are proven, but the
proposed label materially overclaims the observed capability. The selected next
task is exactly
`AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-RELABEL-01`.
