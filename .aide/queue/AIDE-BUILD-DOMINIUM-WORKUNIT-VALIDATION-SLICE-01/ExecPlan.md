# ExecPlan: AIDE-BUILD-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01

## Objective

Build the first post-seam vertical slice that performs exactly one registered
local read-only `dominium.validation.run` capability invocation from a WorkUnit
against a temporary fixture workspace, then records the typed result as
EvidencePacket, EventRecord, and deterministic read-only projection evidence.

## Scope

In scope:

- a bounded `core/interop/dominium/workunit_validation.py` adapter;
- thin `aide_lite.py dominium-workunit-validation` CLI commands;
- fixture input for the temporary workspace;
- generated reports under `.aide/reports/dominium-workunit-validation-slice/`;
- focused tests and task-local evidence.

Out of scope:

- arbitrary shell commands;
- private tool calls;
- broad Dominium command dispatch;
- provider/model/network calls;
- worker execution;
- Workbench behavior;
- Service or durable database state;
- preview/apply/rollback;
- source or target repository mutation.

## Plan

1. Confirm the accepted Dominium read-only seam gate and queue routing.
2. Add a narrow registered capability adapter for `dominium.validation.run`.
3. Generate a temporary fixture workspace and deterministic context records.
4. Build ContextDescriptor, ContextPack, WorkUnit, typed result, EvidencePacket,
   EventRecord, and projection outputs.
5. Validate exactly one invocation, no forbidden boundary crossing, unchanged
   fixture workspace state, and deterministic output.
6. Materialize task evidence, stop at `needs_review`, and recommend exactly
   `AIDE-CHECK-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01`.

## Progress

- [x] Baseline and predecessor routing checked.
- [x] Bounded capability adapter implemented.
- [x] CLI run/status/validate commands added.
- [x] Fixture and report outputs generated.
- [x] Focused tests added.
- [x] Task evidence materialized.
- [ ] Independent check completed.
- [ ] Acceptance completed.

## Exit

Result is `PASS_WITH_WARNINGS`; the build stops at `needs_review` and the only
recommended next task is `AIDE-CHECK-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01`.
