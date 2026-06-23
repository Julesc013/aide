# ExecPlan: AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01

## Objective

Build a minimal domain-neutral `RegisteredProcessExecutionProvider` v0 from the
accepted Dominium command-boundary proof while preserving Dominium behavior
through a thin adapter.

## Scope

- `core/execution/**`
- `core/protocol/process_invocation.py`
- `core/protocol/execution_receipt.py`
- `core/protocol/__init__.py`
- `core/interop/dominium/registered_validation_backend.py`
- focused provider and Dominium parity tests
- task-local reports, evidence, queue index, and root logs

## Dependencies

- `AIDE-ACCEPT-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01` at commit `0754363`.
- Accepted source capability:
  `dominium_registered_validation_command_boundary_invocation_v0`.

## Plan

1. Add neutral invocation, binding, outcome, and receipt records.
2. Add a registered process provider that validates immutable specs, performs
   preflight, constructs exact argv, launches once with `shell=False`, captures
   scrubbed stream summaries, invokes injected probes and decoders, and emits a
   neutral receipt.
3. Refactor the Dominium adapter to own domain identity, argument plan,
   preflight, state probe, JSON decoding, refusal mapping, and evidence
   projection while delegating process mechanics to the provider.
4. Add focused generic-provider tests and Dominium parity tests.
5. Write task evidence and stop at `needs_review`.

## Verification

Compile changed Python, run focused provider tests, run focused Dominium parity
tests, validate existing registered-validation reports, run no-domain-name scan
over generic provider sources, run local-path and secret-like scans, inspect task
evidence, run broad validation, and run diff/commit-policy checks.

## Stop Condition

Stop at `needs_review` with `PASS_WITH_WARNINGS` and recommend only
`AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01`.
