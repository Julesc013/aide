# AIDE-CHECK-AIDE-SELF-VALIDATION-PROCESS-ADAPTER-01

Create and process `AIDE-CHECK-AIDE-SELF-VALIDATION-PROCESS-ADAPTER-01`.

Independently check `AIDE-BUILD-AIDE-SELF-VALIDATION-PROCESS-ADAPTER-01`.

Verify that the adapter reuses the unchanged RegisteredProcessExecutionProvider v0,
spawns exactly one allowlisted AIDE Lite validate process for the successful run,
derives its typed result from process stdout, preserves the shared ProcessExecutionReceipt
and CapabilityOutcome model, refuses unsupported capabilities before process creation,
does not mutate the AIDE workspace across the invocation, and keeps committed reports
free of absolute local paths or secret-like values.

Do not accept the provider in this check. If all material checks pass, recommend exactly:

AIDE-BUILD-EUREKA-READONLY-PROCESS-ADAPTER-01
