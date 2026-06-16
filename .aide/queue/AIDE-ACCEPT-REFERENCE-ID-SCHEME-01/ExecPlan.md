# ExecPlan: AIDE-ACCEPT-REFERENCE-ID-SCHEME-01

## Objective

Perform a check-only acceptance review for the stable AIDE Reference ID Scheme chain and accept only the `minimal_reference_id_scheme` capability if the live build/check evidence supports it.

## Scope

- Review `AIDE-BUILD-REFERENCE-ID-SCHEME-01` and `AIDE-CHECK-REFERENCE-ID-SCHEME-01`.
- Review the ReferenceID schema, helper, CLI dispatch, generated reports, reference map, tests, and predecessor compatibility evidence.
- Write acceptance evidence under `.aide/queue/AIDE-ACCEPT-REFERENCE-ID-SCHEME-01/evidence/`.
- Write acceptance reports under `.aide/reports/reference-id-accept/`.
- Add the task to `.aide/queue/index.yaml`.
- Update `PLANS.md` and `IMPLEMENT.md`.
- Stop at `needs_review`.

## Non-Goals

No ReferenceID repair, EventRecord implementation, OKF knowledge bundle, Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, runtime reference registry, resolver service, database state, leases, scheduler, supervisor, Test Broker runtime, async execution, worker execution, Service, Commander, provider adapters, branch/worktree automation, target apply, active apply, rollback, uninstall, release, promotion, GitHub mutation, Gateway calls, network calls, model/provider calls, production readiness, release readiness, or broad autonomous runtime.

## Allowed Paths

- `.aide/queue/AIDE-ACCEPT-REFERENCE-ID-SCHEME-01/**`
- `.aide/reports/reference-id-accept/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

All implementation files, build/check task files, predecessor protocol schemas, and prior reports are read-only review inputs.

## Progress

- Live queue truth verified: the build and check tasks are present, indexed, and complete at `needs_review`.
- `.aide/context/latest-task-packet.md` verified stale relative to queue truth; it points at lifecycle-runner work and is not authority for this acceptance.
- Build evidence reviewed: result `PASS_WITH_WARNINGS`, missing evidence 0, projected refs 25, required locator misses 0, required locator SHA-256 misses 0.
- Check evidence reviewed: result `PASS_WITH_WARNINGS`, missing evidence 0, no blocking findings.
- Preflight validation rerun with a corrected command wrapper after an initial wrapper invocation failed before running commands.
- Out-of-scope generated report churn from preflight was restored before acceptance artifacts were written.

## Decisions

- Accept `minimal_reference_id_scheme` with warnings.
- Treat full Draft 2020-12 JSON Schema validation, runtime resolution, EventRecord, OKF, PatchTransaction, adapters, ContextPack v2, and runtime coordination as explicit non-capabilities.
- Recommend exactly `AIDE-BUILD-EVENT-RECORD-SCHEMA-01` after acceptance.

## Validation Intent

Run git whitespace checks, JSON parsing for the acceptance report, task inspect/evidence for the acceptance task, ReferenceID status/validate, predecessor validators, broad repository validation, overclaim scans, and commit policy validation.

## Recovery

This task is idempotent. If interrupted, re-run the validation commands, check for generated report churn, and update the acceptance evidence and reports without changing ReferenceID implementation files.

## Stop State

End at `needs_review` with result `ACCEPTED_WITH_WARNINGS`.
