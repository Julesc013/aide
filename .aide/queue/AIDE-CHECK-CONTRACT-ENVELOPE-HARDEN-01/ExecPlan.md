# ExecPlan

## Objective

Independently review the schema runtime validation hardening from
`AIDE-BUILD-CONTRACT-ENVELOPE-HARDEN-01`.

## Scope

This is a check-only task. It may write only the check WorkUnit, check reports,
and queue index entry. It must not repair implementation defects inline.

## Non-Goals

- No implementation code changes.
- No EvidencePacket, WorkUnit, TestJob, Checkpoint, Service, Commander,
  provider, branch/worktree, target apply, active apply, rollback execution,
  release, Gateway, network, GitHub, or model/provider work.

## Plan

1. Verify live repo state and reported commits.
2. Review the protocol helper, schema, CLI dispatch, focused tests, reports,
   and HARDEN-01 evidence.
3. Run focused unit tests, command validation, and direct negative runtime
   checks in temp/in-memory contexts.
4. Compare hardening claims to observed evidence.
5. Write check report and evidence.
6. Restore out-of-scope generated churn, commit check artifacts if policy
   permits, and stop at `needs_review`.

## Progress

- [x] Preflight completed.
- [x] Static implementation review completed.
- [x] Runtime schema and negative checks completed.
- [x] Tests and validation completed.
- [x] Check reports and evidence written.
- [ ] Commit check artifacts and run commit policy check.

## Review Gate

The task stops at `needs_review`.
