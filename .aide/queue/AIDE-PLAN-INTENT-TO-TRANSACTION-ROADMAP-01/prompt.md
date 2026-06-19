# AIDE-PLAN-INTENT-TO-TRANSACTION-ROADMAP-01

Create and process `AIDE-PLAN-INTENT-TO-TRANSACTION-ROADMAP-01`.

Use `.aide/queue/index.yaml` as canonical queue truth. Re-read the live
repository before writing anything.

## Goal

Incorporate the 2026-06-19 through 2026-06-20 architecture synthesis into
AIDE's roadmap and planning records.

The plan should preserve that AIDE is a portable intent-to-transaction control
plane. AIDE owns identity, context, governance, routing, evidence, events,
capability admission, transaction envelopes, and shared projections. Domains
own product semantics. Hosts present and request actions. Capability providers
perform admitted deterministic operations.

## Required Planning Decisions

- Preserve the current serialized next task from live queue truth.
- Keep PatchTransaction v1 file-oriented and no-apply.
- Add CapabilityInvocation before broad Host Contract execution.
- Add a Host Contract v0 lane before broad Workbench implementation.
- Add a Dominium integration charter and bridge conformance lane before
  Dominium-specific Workbench mutation.
- Add DevelopmentTransaction and PreviewSession/ShadowWorkspace before
  Workbench mutation work.
- Prefer validation and document preview slices before scene mutation.
- Require every new contract family to justify itself through a narrow
  executable vertical slice.

## Non-Goals

Do not implement schemas, helpers, commands, tests, Host SDK, Host Contract,
CapabilityInvocation, DevelopmentTransaction, PreviewSession, ShadowWorkspace,
Dominium Bridge conformance, Workbench, Commander, Service, runtime, worker
execution, provider/model calls, network calls, patch apply, branch/worktree
automation, target mutation, release, or promotion.

## Exit Criteria

Stop at `needs_review`. Recommend exactly the live serialized next task unless
live queue truth changes during execution.
