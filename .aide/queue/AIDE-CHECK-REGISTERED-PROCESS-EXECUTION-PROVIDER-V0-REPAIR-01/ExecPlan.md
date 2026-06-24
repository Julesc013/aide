# ExecPlan: AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01

## Objective

Independently check the bounded repair from
`AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01` without
repairing implementation or accepting the proposed provider.

## Scope

- Task-local independent behavior harness and evidence.
- Check report under `.aide/reports/registered-process-execution-provider-v0-repair-check/`.
- Queue index entry plus focused root planning and implementation logs.

No provider, protocol, Dominium adapter, or focused test implementation files are
in scope for mutation.

## Source Findings To Close

1. Binding mismatches launch a process.
2. Launch accounting is cumulative or stale across provider reuse.
3. Decoder failures report complete validation/evidence axes.
4. State-probe failures report complete typed results.
5. Cancellation is neither implemented nor declared unsupported.

## Plan

1. Inspect the repair task, source failed check, implementation, tests, queue
   policy, queue index, `PLANS.md`, and `IMPLEMENT.md`.
2. Run a task-local independent harness with fake runners, fake probes, and
   fake decoders only.
3. Run focused provider and Dominium parity tests.
4. Verify genericity, non-overclaiming, scrubbed reports, broad validation, task
   inspect/evidence, and diff checks.
5. Record result and stop at `needs_review`.

## Non-Capabilities

This task does not repair implementation, accept the provider, implement
cancellation, add new adapters, rerun the live Dominium command, mutate Dominium
or target repositories, call providers/models/network services, run workers,
start Service/Workbench/runtime behavior, preview/apply/rollback, create
branches/worktrees, mutate GitHub, release, or promote.

## Exit Criteria

Stop at `needs_review` with one of the task-allowed result values.

If material findings remain, recommend exactly:

```text
AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-02
```

If the repair passes, recommend exactly:

```text
AIDE-BUILD-AIDE-SELF-VALIDATION-PROCESS-ADAPTER-01
```
