# ExecPlan

## Objective

Introduce a minimal public protocol envelope from the accepted lifecycle fixture
runner slice.

## Scope

This is a protocol-shaped vertical slice, not a kernel scaffold. The work may
add a narrow helper, schema, CLI dispatch, projections of existing lifecycle
fixture reports, focused tests, queue evidence, and contract-envelope reports.

## Non-Goals

- No full AIDE kernel schema suite.
- No WorkUnit CLI, Test Broker, Codex adapter, Service, Commander, provider
  adapter, branch/worktree automation, target repo apply, active repo apply,
  rollback execution, uninstall execution, release, promotion, network,
  Gateway, GitHub, or model/provider calls.
- No destructive migration of existing lifecycle runner reports.

## Plan

1. Verify the accepted lifecycle fixture runner predecessor and repo state.
2. Add a minimal `apiVersion` / `kind` / `metadata` / `spec` / `status`
   envelope helper.
3. Project lifecycle fixture run, verify, and acceptance reports into additive
   envelope reports.
4. Add thin AIDE Lite CLI dispatch for `contract-envelope status`, `project`,
   and `validate`.
5. Add focused tests for envelope validation, compatibility, projections, and
   parser behavior.
6. Generate reports and evidence.
7. Run validation, commit if policy permits, and stop at `needs_review`.

## Progress

- [x] Preflight and predecessor acceptance reviewed.
- [x] Minimal helper and schema added.
- [x] CLI dispatch added.
- [x] Focused tests added.
- [x] Reports and evidence prepared.
- [x] Validation completed.

## Review Gate

The task stops at `needs_review`.

## Recovery

If interrupted, inspect `status.yaml`, the diff, and
`.aide/reports/contract-envelope/`. Do not continue into WorkUnit CLI, Test
Broker, Service, Commander, provider adapters, branch/worktree automation,
target repo apply, rollback execution, release, Gateway, network, or
model/provider work.
