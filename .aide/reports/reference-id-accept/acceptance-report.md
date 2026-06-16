# ReferenceID Acceptance Report

- task_id: AIDE-ACCEPT-REFERENCE-ID-SCHEME-01
- status: ACCEPTED_WITH_WARNINGS
- planning_state: acceptance_review_completed
- review_gate: needs_review
- check_only: true
- authorizes_implementation: false
- accepted_capability: minimal_reference_id_scheme
- recommended_next_task: AIDE-BUILD-EVENT-RECORD-SCHEMA-01

## Summary

The stable AIDE Reference ID Scheme is accepted with warnings as `minimal_reference_id_scheme`.

The accepted capability is limited to stable `aide://<kind>/<id>` identity syntax, ReferenceID schema/helper/projection/validation, thin `reference-id status/project/validate` CLI dispatch, deterministic reference-map reports, file paths as locators, optional SHA-256 locator metadata, and required-vs-optional unknown-kind behavior.

## Source Chain

- `AIDE-ACCEPT-TESTJOB-SCHEMA-01`: ACCEPTED_WITH_WARNINGS.
- `AIDE-BUILD-REFERENCE-ID-SCHEME-01`: PASS_WITH_WARNINGS.
- `AIDE-CHECK-REFERENCE-ID-SCHEME-01`: PASS_WITH_WARNINGS.

## Evidence

- Build evidence missing: 0.
- Check evidence missing: 0.
- Projected refs: 25.
- Required locators missing: 0.
- Required locators without SHA-256: 0.
- All projected refs parse: true.
- Source artifacts mutated: false.
- Predecessor compatibility preserved: true.
- Overclaiming check passed: true.
- Forbidden operations preserved: true.

## Warnings

- ReferenceID is syntactic/projection-only and does not implement runtime resolution.
- Full Draft 2020-12 JSON Schema validation remains deferred.
- Runtime reference registry/resolver service is not implemented.
- EventRecord is not implemented.
- OKF, Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, and runtime coordination remain future work.
- `.aide/context/latest-task-packet.md` remains stale relative to queue truth.

All warnings are non-blocking for the accepted capability.

## Boundary

This acceptance does not authorize EventRecord implementation, OKF, Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, runtime registry, resolver service, database state, leases, scheduler, supervisor, Test Broker runtime, async execution, worker execution, Service, Commander, provider adapters, branch/worktree automation, target apply, active apply, rollback, uninstall, release, promotion, GitHub mutation, Gateway calls, network calls, model/provider calls, production readiness, release readiness, or broad autonomous runtime.
