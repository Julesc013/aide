# ExecPlan: AIDE-BUILD-REFERENCE-ID-SCHEME-01

## Objective

Build the minimal metadata-only `ReferenceID` scheme after the accepted `minimal_test_job_schema` capability.

## Scope

- Add `.aide/protocol/aide-reference-id.schema.json`.
- Add `core/protocol/reference_id.py` for `aide://<kind>/<id>` parsing, validation, reference-record construction, projection, and report generation.
- Add thin `reference-id status/project/validate` dispatch in `.aide/scripts/aide_lite.py`.
- Add focused ReferenceID tests.
- Write reports under `.aide/reports/reference-id/`.
- Write task evidence and stop at `needs_review`.

## Non-Goals

No EventRecord implementation, OKF knowledge bundle, reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, runtime reference registry, resolver service, database state, leases, scheduler, supervisor, Test Broker runtime, async execution, worker execution, Service, Commander, provider adapters, branch/worktree automation, active repo apply, target apply, rollback execution, uninstall execution, release, promotion, GitHub mutation, Gateway calls, network calls, model/provider calls, production readiness, release readiness, or broad autonomous runtime.

## Verification Intent

Use focused ReferenceID tests, schema JSON parsing, Python compile checks, `reference-id status/project/validate`, predecessor protocol validation commands, task inspect/evidence, boundary scans, `git diff --check`, and commit policy validation.

## Stop State

End at `needs_review`; recommended next task is `AIDE-CHECK-REFERENCE-ID-SCHEME-01`.
