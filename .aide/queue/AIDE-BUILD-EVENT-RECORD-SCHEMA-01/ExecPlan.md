# ExecPlan: AIDE-BUILD-EVENT-RECORD-SCHEMA-01

## Objective

Build the minimal projection-only `EventRecord` protocol slice after accepted `minimal_reference_id_scheme`.

## Scope

- Add `.aide/protocol/aide-event-record.schema.json`.
- Add `core/protocol/event_record.py` for EventRecord construction, validation, event family projection, example projection, and report generation.
- Add thin `event-record status/project/validate` dispatch in `.aide/scripts/aide_lite.py`.
- Add focused EventRecord tests.
- Write reports under `.aide/reports/event-record/`.
- Write task evidence and stop at `needs_review`.

## Non-Goals

No event sourcing runtime, append-only runtime event store, runtime event log, state reconstruction, scheduler, leases, supervisor, Test Broker runtime, async execution, worker execution, Service, Commander, OKF knowledge bundle, Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, runtime reference registry, resolver service, database state, provider adapters, branch/worktree automation, target apply, active apply, rollback execution, uninstall execution, release, promotion, GitHub mutation, Gateway calls, network calls, model/provider calls, target repo mutation, production readiness, release readiness, or broad autonomous runtime.

## Allowed Paths

Use the allowlist in `task.yaml`. Predecessor ReferenceID, TestJob, WorkerRun, WorkUnit, EvidencePacket, and ContractEnvelope artifacts are read-only inputs except for deterministic validation churn that must be restored if outside this task scope.

## Current Facts

- `AIDE-ACCEPT-REFERENCE-ID-SCHEME-01` is `ACCEPTED_WITH_WARNINGS` and recommends this task.
- `.aide/context/latest-task-packet.md` is stale lifecycle-runner text and is not authority for this slice.
- The accepted ReferenceID capability is syntactic/projection-only and supplies stable `aide://...` refs used by EventRecord.

## Milestones

- Live queue and predecessor state verified.
- EventRecord schema/helper added.
- Thin CLI dispatch added.
- Event family index, projection report, validation report, and projection-only examples generated.
- Focused tests passed.
- Evidence written.
- Task stopped at review with next task `AIDE-CHECK-EVENT-RECORD-SCHEMA-01`.

## Validation Intent

Use Python compile checks, EventRecord focused tests, schema/report JSON parsing, `event-record status/project/validate`, `reference-id validate`, predecessor protocol validators, task inspect/evidence, overclaim scans, broad repository validation, diff whitespace checks, and commit policy validation.

## Progress

- 2026-06-17: Preflight verified clean `main` at `af6429133767707ae8da4f466e0018202854103f`; ReferenceID acceptance exists and live Task OS latest-task packet remains stale.
- 2026-06-17: Implemented EventRecord schema/helper/CLI/tests and generated EventRecord reports.
- 2026-06-17: Focused EventRecord tests passed; full validation is recorded in task evidence.

## Decisions

- Event identity is `aide://event/<id>`.
- Subject, causation, correlation, actor, evidence, and report links use ReferenceID validation where practical.
- Example events are report projections only; they are not appended to a runtime log.
- Event family names reserve vocabulary only and do not implement their named subsystems.

## Recovery

The task is restartable from the queue packet. Re-run `py -3 .aide/scripts/aide_lite.py event-record validate` to regenerate `.aide/reports/event-record/**`, then re-run focused tests and predecessor validators before updating evidence.

## Stop State

End at `needs_review`; recommended next task is exactly `AIDE-CHECK-EVENT-RECORD-SCHEMA-01`.
