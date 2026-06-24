# AIDE-CHECK-EUREKA-READONLY-PROCESS-ADAPTER-01

Create and process `AIDE-CHECK-EUREKA-READONLY-PROCESS-ADAPTER-01`.

This is an independent check-only task for
`AIDE-BUILD-EUREKA-READONLY-PROCESS-ADAPTER-01` at commit `961add0`.

Do not repair implementation.
Do not accept `RegisteredProcessExecutionProvider v0`.
Do not invoke the live Eureka process a second time.

Verify provider immutability, selected command authenticity, exact invocation
evidence, result origin, state safety, cross-adapter reuse, leakage hygiene,
focused regressions, broad validation, and complete task evidence.

If material findings remain, recommend exactly:

```text
AIDE-BUILD-EUREKA-READONLY-PROCESS-ADAPTER-REPAIR-01
```

If the check passes, recommend exactly:

```text
AIDE-ACCEPT-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01
```
