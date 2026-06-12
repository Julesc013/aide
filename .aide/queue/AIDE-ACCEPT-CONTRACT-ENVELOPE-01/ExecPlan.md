# ExecPlan

## Objective

Perform a check-only acceptance review for the minimal contract envelope chain:
BUILD, CHECK, HARDEN, and HARDEN-CHECK.

## Scope

The accepted capability, if validated, is only the minimal contract envelope:
`apiVersion`, `kind`, `metadata`, `spec`, `status`, the focused helper,
minimal schema subset runtime validation, helper/schema alignment,
lifecycle-fixture report projections, and `contract-envelope status/project/validate`.

## Non-Goals

- No implementation code changes.
- No EvidencePacket, WorkUnit, TestJob, Test Broker, Service, Commander,
  provider, branch/worktree, target apply, active apply, rollback execution,
  release, promotion, network, Gateway, GitHub, or model/provider behavior.

## Plan

1. Verify reported commits and queue task evidence.
2. Review the protocol helper, schema, CLI dispatch, focused tests, reports,
   and prior check/harden evidence.
3. Run focused tests, lifecycle compatibility checks, direct negative behavior
   checks, and repo validation.
4. Write the acceptance WorkUnit evidence and acceptance reports.
5. Mark reviewed contract-envelope tasks accepted according to the existing
   queue convention and stop this acceptance task at `needs_review`.
6. Restore incidental generated report churn and commit acceptance artifacts.

## Progress

- [x] Preflight completed.
- [x] Static acceptance review completed.
- [x] Dynamic validation and negative checks completed.
- [x] Acceptance reports and evidence written.
- [x] Commit acceptance artifacts and run commit policy check.

## Review Gate

This task stops at `needs_review`.
