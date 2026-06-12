# ExecPlan

## Objective

Introduce the minimal EvidencePacket schema and projection slice earned by the
accepted lifecycle fixture runner and accepted contract-envelope artifacts.

## Scope

This is a protocol-shaped vertical slice, not an evidence engine. The work may
add a narrow helper, schema, CLI dispatch, projections of existing accepted
reports, focused tests, queue evidence, and EvidencePacket reports.

## Non-Goals

- No full evidence engine or EvidenceStore.
- No WorkUnit schema, WorkUnit CLI, TestJob schema, Test Broker, Checkpoint,
  PromotionPolicy, Service, Commander, provider adapters, branch/worktree
  automation, target repo apply, active repo apply, rollback execution,
  uninstall execution, release, promotion, network, Gateway, GitHub, or
  model/provider calls.
- No destructive migration of accepted lifecycle runner or contract-envelope
  reports.

## Plan

1. Verify accepted predecessor task and current repo state.
2. Add a minimal `EvidencePacket` helper and schema under `core/protocol` and
   `.aide/protocol/`.
3. Project accepted lifecycle runner and contract-envelope reports into
   additive EvidencePacket JSON objects.
4. Add thin AIDE Lite CLI dispatch for `evidence-packet status`, `project`, and
   `validate`.
5. Add focused tests for helper validation, schema alignment, projections,
   explicit non-capabilities, and parser behavior.
6. Generate reports and queue evidence.
7. Run validation, commit if policy permits, and stop at `needs_review`.

## Progress

- [x] Preflight and predecessor acceptance reviewed.
- [x] Minimal helper and schema added.
- [x] CLI dispatch added.
- [x] Focused tests added.
- [x] Reports and projections generated.
- [x] Queue evidence prepared.
- [x] Final validation completed.
- [ ] Commit completed.

## Review Gate

The task stops at `needs_review`.

## Recovery

If interrupted, inspect `status.yaml`, the diff, and
`.aide/reports/evidence-packet/`. Do not continue into WorkUnit CLI, Test
Broker, Service, Commander, provider adapters, branch/worktree automation,
target repo apply, rollback execution, release, Gateway, network, or
model/provider work.
