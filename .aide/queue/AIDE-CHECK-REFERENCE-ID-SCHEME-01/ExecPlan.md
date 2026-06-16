# ExecPlan: AIDE-CHECK-REFERENCE-ID-SCHEME-01

## Objective

Independently check `AIDE-BUILD-REFERENCE-ID-SCHEME-01` without modifying implementation code.

## Scope

- Review the ReferenceID schema, helper, CLI dispatch, generated reports, reference map, tests, and build evidence.
- Generate check-only reports under `.aide/reports/reference-id-check/`.
- Generate task-local evidence under `.aide/queue/AIDE-CHECK-REFERENCE-ID-SCHEME-01/evidence/`.
- Update queue index and root plan/execution logs because the check is a substantial queue item.
- Stop at `needs_review`.

## Non-Goals

No implementation repairs, EventRecord, OKF, Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, runtime reference registry, resolver service, database state, leases, scheduler, supervisor, Test Broker runtime, async execution, worker execution, Service, Commander, provider adapters, branch/worktree automation, target apply, active apply, rollback, uninstall, release, promotion, GitHub mutation, Gateway calls, network calls, model/provider calls, production readiness, release readiness, or broad autonomous runtime.

## Allowed Paths

- `.aide/queue/AIDE-CHECK-REFERENCE-ID-SCHEME-01/**`
- `.aide/reports/reference-id-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

All build implementation files and predecessor protocol artifacts are read-only review inputs.

## Progress

- Live queue truth verified: `AIDE-BUILD-REFERENCE-ID-SCHEME-01` exists, is indexed, and reports `PASS_WITH_WARNINGS`.
- Build evidence verified: task inspect/evidence reports complete with missing evidence 0.
- ReferenceID live commands rerun: status/project/validate returned `PASS_WITH_WARNINGS`.
- Predecessor validators rerun and passed.
- Preflight generated report churn was restored before check artifacts were written.

## Validation Intent

Run focused compile, unittest, JSON parsing, ReferenceID commands, predecessor validators, task evidence checks, overclaim scans, broad repo validation, diff whitespace checks, and commit policy validation.

## Stop State

End at `needs_review` with result `PASS_WITH_WARNINGS`; recommended next task is `AIDE-ACCEPT-REFERENCE-ID-SCHEME-01`.
