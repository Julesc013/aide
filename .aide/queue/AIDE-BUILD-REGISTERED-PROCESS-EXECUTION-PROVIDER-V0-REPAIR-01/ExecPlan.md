# ExecPlan: AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01

## Objective

Repair only the five material safety findings from
`AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01` and stop at
`needs_review` with the provider still proposed and unaccepted.

## Scope

- Generic provider safety behavior in `core/execution/registered_process.py`.
- Focused provider regression tests in
  `.aide/scripts/tests/test_aide_registered_process_provider.py`.
- Existing Dominium parity tests, run but not broadened.
- Task-local evidence and repair reports for this queue item.
- Queue index plus root planning/execution logs.

## Source Findings

The source check recorded `REQUEST_CHANGES` with five material findings:

1. Mismatched capability/provider bindings can still launch.
2. Reused provider instances can emit cumulative or stale launch receipts.
3. Decoder exceptions can report complete validation/evidence axes.
4. State-probe failures can report complete typed domain results.
5. Cancellation is neither implemented nor declared unsupported.

## Plan

1. Add pre-launch binding/provider/spec coherence validation.
2. Make launch accounting and launch metadata per invocation.
3. Mark decoder exceptions and other undecoded outcomes incomplete.
4. Make state-probe failures fail closed without preserving typed domain output.
5. Declare process cancellation as an explicit v0 non-capability.
6. Add focused regression coverage for all repaired findings.
7. Preserve Dominium parity through existing focused tests.
8. Write task evidence, update queue index and logs, validate, and commit.

## Non-Capabilities

This task does not accept the provider, implement cancellation, add Omnigent or
ExecutionHost behavior, run workers, start services, call providers/models or
network services, rerun the live Dominium command, mutate Dominium or target
repositories, apply transactions, create branches/worktrees, mutate GitHub, or
publish releases.

## Exit Criteria

Stop at `needs_review` with `PASS_WITH_WARNINGS`, complete task evidence, and
recommended next task exactly:

```text
AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01
```
