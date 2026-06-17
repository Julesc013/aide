# ExecPlan: AIDE-ACCEPT-EVENT-RECORD-SCHEMA-01

## Objective

Perform a check-only acceptance review for the projection-only `minimal_event_record_schema` capability.

## Scope

- Review `AIDE-ACCEPT-REFERENCE-ID-SCHEME-01`, `AIDE-BUILD-EVENT-RECORD-SCHEMA-01`, and `AIDE-CHECK-EVENT-RECORD-SCHEMA-01`.
- Classify build and check warnings as blocking or non-blocking.
- Accept only the schema/helper/projection/validation/CLI/report/test surface supported by evidence.
- Generate task-local acceptance evidence and `.aide/reports/event-record-accept/**`.
- Update the queue index, plan index, and implementation log.
- Stop at `needs_review`.

## Non-Goals

No EventRecord implementation repair, event sourcing runtime, append-only runtime store, runtime event log, state reconstruction, replay, scheduler, leases, supervisor, Test Broker runtime, async execution, worker execution, Service, Commander, OKF implementation, Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, runtime reference registry, resolver service, database state, provider adapters, branch/worktree automation, target apply, active apply, rollback, uninstall, release, promotion, GitHub mutation, Gateway calls, network calls, model/provider calls, target repo mutation, production readiness, release readiness, or broad autonomous runtime.

## Allowed Paths

Use the allowlist in `task.yaml`. Build/check EventRecord artifacts and predecessor protocol files are read-only review inputs.

## Current Facts

- Initial HEAD for this acceptance review was `6a79172ea5806196b4499686f3804fddf4a7e493`.
- `AIDE-BUILD-EVENT-RECORD-SCHEMA-01` completed with `PASS_WITH_WARNINGS`.
- `AIDE-CHECK-EVENT-RECORD-SCHEMA-01` completed with `PASS_WITH_WARNINGS`.
- Build and check evidence are complete with 0 missing evidence files.
- `.aide/context/latest-task-packet.md` remains stale lifecycle-runner text and is not authority.

## Milestones

- Live queue truth verified.
- Build and check evidence reviewed.
- EventRecord schema/helper/projection/CLI/tests reviewed.
- Warnings classified as non-blocking.
- Acceptance reports and next OKF prompt written.
- Validation completed and task stopped at `needs_review`.

## Validation Intent

Run task inspect/evidence checks, EventRecord status/project/validate, schema/report JSON parsing, predecessor validators, broad repository validation, acceptance report JSON parsing, and Git diff checks.

## Progress

- 2026-06-17: Preflight verified clean `main` at `6a79172ea5806196b4499686f3804fddf4a7e493`.
- 2026-06-17: Source chain reviewed; no blocking findings found.
- 2026-06-17: Acceptance result set to `ACCEPTED_WITH_WARNINGS`.

## Decisions

- Accept `minimal_event_record_schema` only.
- Event families are accepted as reserved vocabulary with `implemented_subsystem: false`.
- Example events are accepted only as projection-only records with `recorded: false`.
- OKF is the next build task after acceptance, but this task does not implement OKF.

## Recovery

Re-run the validation commands recorded in `evidence/test-and-validation-review.md`; if any source chain evidence becomes missing or validation fails, change result to the appropriate not-accepted state before review.

## Stop State

End at `needs_review`; recommended next task is `AIDE-BUILD-OKF-KNOWLEDGE-BUNDLE-01`.
