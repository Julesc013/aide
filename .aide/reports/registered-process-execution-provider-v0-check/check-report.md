# Registered Process Execution Provider v0 Check

- task_id: `AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01`
- result: `REQUEST_CHANGES`
- material_finding_count: `5`
- missing_evidence: `0`
- recommended_next_task: `AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01`

## Findings

### binding.mismatch_launches_process

- severity: `material`
- summary: Mismatched capability/provider bindings still launch a process instead of failing closed before launch.

### receipt.launch_accounting_is_cumulative_or_stale

- severity: `material`
- summary: Receipt launcher accounting and launch metadata are not per-invocation when a provider instance is reused.

### decoder.failure_marked_complete

- severity: `material`
- summary: Decoder exceptions are represented, but validation and evidence axes still report complete.

### state_probe.failure_not_failed_closed

- severity: `material`
- summary: State-probe failure is recorded in the receipt but the outcome still reports a complete typed result.

### cancellation.not_implemented_or_declared

- severity: `material`
- summary: The receipt has a cancelled field, but cancellation support is neither implemented nor listed as an explicit non-capability.
