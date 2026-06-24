# AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-01

Independently check `AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-01`.

This is check-only. Do not repair implementation.

Verify the bounded LocalProcessExecutionHost v0 build for:

- accepted ExecutionHost contract alignment;
- fixture-only scope;
- exact process boundary;
- workspace containment;
- event truth;
- artifact truth;
- lifecycle state truth;
- process/worker/event/artifact/evidence/acceptance outcome separation;
- no overclaiming;
- source tests and regression validation.

If material findings remain, recommend exactly:

```text
AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-01
```

If all material checks pass, recommend exactly:

```text
AIDE-ACCEPT-LOCAL-PROCESS-EXECUTION-HOST-V0-01
```

Stop at `needs_review`.
