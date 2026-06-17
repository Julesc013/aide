# ExecPlan: AIDE-CHECK-OKF-KNOWLEDGE-BUNDLE-01

## Objective

Independently check `AIDE-BUILD-OKF-KNOWLEDGE-BUNDLE-01` as a bounded, check-only WorkUnit. The check reviews the OKF-compatible knowledge bundle, generated reports, CLI surface, predecessor integration, tests, validation, and authority boundaries without repairing implementation files.

## Scope

Allowed writes are limited to this check task directory, `.aide/reports/okf-check/**`, `.aide/queue/index.yaml`, `PLANS.md`, and `IMPLEMENT.md`. The OKF bundle and implementation sources are read-only except for deterministic projection verification; any resulting generated churn must be classified and contained.

## Dependencies

- `AIDE-BUILD-OKF-KNOWLEDGE-BUNDLE-01` is `needs_review` with result `PASS_WITH_WARNINGS`.
- The reported build commit is `c51859006e8cf4ac429bbaf9663917d0fdbe904b`, which is an ancestor of the live HEAD reviewed for this check.
- EventRecord and ReferenceID predecessor validation surfaces remain warning-only.

## Plan

1. Verify live repository and queue state before edits.
2. Review build task metadata, evidence, OKF reports, CLI integration, tests, and generated concept/link indexes.
3. Run deterministic OKF projection and validation checks without accepting generated churn outside the check scope.
4. Record review evidence and `okf-check` reports.
5. Stop at `needs_review` and recommend `AIDE-ACCEPT-OKF-KNOWLEDGE-BUNDLE-01`.

## Progress

- [x] Live repo state inspected.
- [x] Build task and OKF reports reviewed.
- [x] Generated pre-check status/report churn restored where outside scope.
- [x] Check task and report artifacts written.
- [x] Final validation run after artifact creation.
- [x] Commit-ready artifact set prepared.

## Review Boundary

This task does not authorize implementation repair, OKF runtime behavior, Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, runtime services, provider/model calls, branch mutation, target mutation, release work, or GitHub mutation.

## Exit Criteria

The task exits when required evidence exists, `check-report.json` parses, OKF validation and lint remain `PASS_WITH_WARNINGS`, task evidence inspection is complete, generated churn is contained, and the queue item is left at `needs_review`.
