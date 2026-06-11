# ExecPlan

## Objective

Harden the minimal contract envelope slice by wiring the checked-in envelope
schema into runtime validation.

## Scope

This is schema/runtime alignment for the existing lifecycle fixture envelope
projection only. The work may touch the protocol helper, thin CLI output,
focused tests, generated contract-envelope reports, hardening reports, queue
evidence, and planning/execution logs.

## Non-Goals

- No full JSON Schema engine.
- No EvidencePacket, WorkUnit, TestJob, Checkpoint, or PromotionPolicy schema.
- No WorkUnit CLI, Test Broker, Service, Commander, provider adapter,
  branch/worktree automation, target repo apply, active repo apply, rollback
  execution, release, promotion, network, Gateway, GitHub, or model/provider
  calls.
- No destructive migration of accepted lifecycle fixture reports.

## Plan

1. Verify predecessor build/check commits and current repo state.
2. Add stdlib-only schema loading and minimal JSON Schema subset validation.
3. Add schema/helper alignment checks and runtime validation result fields.
4. Update `contract-envelope validate` reports and CLI output truthfully.
5. Add focused tests for schema validation execution and helper/schema agreement.
6. Generate hardening reports and queue evidence.
7. Run validation, commit if policy permits, and stop at `needs_review`.

## Progress

- [x] Preflight and predecessor check reviewed.
- [x] Minimal schema loader and subset validator added.
- [x] Schema/helper alignment checks added.
- [x] Contract-envelope validation reports updated.
- [x] Focused tests expanded.
- [x] Hardening reports and evidence prepared.
- [x] Full validation ladder completed.

## Review Gate

This task stops at `needs_review`.

## Recovery

If interrupted, inspect `status.yaml`, the diff, and
`.aide/reports/contract-envelope/validation.json`. Continue only within this
hardening scope; do not proceed into the next protocol object.
