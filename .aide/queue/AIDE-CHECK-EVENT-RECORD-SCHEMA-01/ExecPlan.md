# ExecPlan: AIDE-CHECK-EVENT-RECORD-SCHEMA-01

## Objective

Independently check the projection-only `EventRecord` schema slice from `AIDE-BUILD-EVENT-RECORD-SCHEMA-01` without repairing or changing implementation files.

## Scope

- Review the EventRecord build queue packet, reports, schema, helper, thin CLI dispatch, tests, and predecessor compatibility.
- Run focused EventRecord validation, predecessor protocol validators, JSON parsing, Task OS evidence checks, broad repository validation, and diff checks.
- Write check-only evidence under `.aide/queue/AIDE-CHECK-EVENT-RECORD-SCHEMA-01/evidence/`.
- Write check reports under `.aide/reports/event-record-check/`.
- Update `.aide/queue/index.yaml`, `PLANS.md`, and `IMPLEMENT.md` for queue traceability.

## Non-Goals

No EventRecord implementation repair, schema mutation, helper mutation, CLI mutation, report model change, event sourcing runtime, append-only event store, runtime event log, replay, state reconstruction, scheduler, leases, supervisor, Test Broker runtime, async execution, worker execution, Service, Commander, OKF knowledge bundle, Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, runtime reference registry, resolver service, database state, providers, branch/worktree automation, target apply, active apply, release, promotion, GitHub mutation, Gateway calls, network calls, model/provider calls, target repo mutation, production readiness, release readiness, or broad autonomous runtime.

## Allowed Paths

Use the allowlist in `task.yaml`. EventRecord build artifacts, EventRecord implementation files, and predecessor artifacts are read-only review inputs. Deterministic report churn from validation commands must be restored if it falls outside this check task's output paths.

## Current Facts

- `AIDE-BUILD-EVENT-RECORD-SCHEMA-01` is `needs_review` with result `PASS_WITH_WARNINGS`.
- The checked build commit is `0e686040b18dff32672bc421bbdd95882f9822f0`.
- The EventRecord build reports `recommended_next_task: AIDE-CHECK-EVENT-RECORD-SCHEMA-01`.
- `.aide/context/latest-task-packet.md` remains stale lifecycle-runner text and is not authority for this check.

## Milestones

- Live queue and build state verified.
- Build evidence, schema, helper, projections, CLI, tests, and reports reviewed.
- Predecessor compatibility and validation commands rerun.
- Out-of-scope generated report churn restored.
- Check evidence and reports written.
- Task stopped at `needs_review` with next task `AIDE-ACCEPT-EVENT-RECORD-SCHEMA-01`.

## Validation Intent

Use Python compile checks, focused EventRecord tests, schema/report JSON parsing, `event-record status/project/validate`, `reference-id validate`, predecessor protocol validators, task inspect/evidence checks, broad repository validation, overclaim review, forbidden-operation review, and Git diff whitespace checks.

## Progress

- 2026-06-17: Verified clean `main` at `0e686040b18dff32672bc421bbdd95882f9822f0` before check work.
- 2026-06-17: Reviewed build evidence and EventRecord machine reports; no blocking defects found.
- 2026-06-17: Validation completed with warnings limited to projection-only scope, minimal JSON Schema subset validation, and stale Task OS latest-task state.

## Decisions

- Result is `PASS_WITH_WARNINGS` rather than `PASS` because EventRecord remains intentionally projection-only and the repo validator still has known report-only/stale-pointer warnings.
- The next task is exactly `AIDE-ACCEPT-EVENT-RECORD-SCHEMA-01`.
- OKF remains future work after EventRecord acceptance and is not recommended directly by this check.

## Recovery

The task is restartable from this queue packet. Re-run `py -3 .aide/scripts/aide_lite.py event-record validate`, focused tests, predecessor validators, task inspect/evidence, and broad validation before changing the check result.

## Stop State

End at `needs_review`; recommended next task is exactly `AIDE-ACCEPT-EVENT-RECORD-SCHEMA-01`.
