# Remaining Risks

The accepted provider remains intentionally narrow.

Known non-blocking risk: future ExecutionHost work must not reinterpret
`ProcessExecutionReceipt` as `WorkerRun` identity or treat this provider as a
worker/session host.
