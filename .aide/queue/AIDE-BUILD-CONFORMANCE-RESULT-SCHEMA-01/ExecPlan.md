# AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-01 ExecPlan

## Objective

Build the first minimal AIDE `ConformanceResult` vertical slice for the accepted
`minimal_capability_manifest` ConformanceProfile candidate.

## Scope

- Add `aide-conformance-result.schema.json`.
- Add `core/protocol/conformance_result.py`.
- Register `conformance-result status/project/validate` in `aide_lite.py`.
- Generate deterministic result, result index, case-result index, projection,
  status, validation, future-work, and unfinished-work reports.
- Add focused tests for result validation, profile binding, profile digest,
  aggregation semantics, case-result semantics, CLI dispatch, and no-overclaiming
  boundaries.
- Materialize queue task metadata and evidence.

## Dependencies

- `AIDE-ACCEPT-CONFORMANCE-PROFILE-01` result:
  `ACCEPTED_WITH_WARNINGS`.
- Accepted candidate profile:
  `aide://conformance-profile/minimal_capability_manifest-v1.0.0`.
- Existing CapabilityManifest, ReferenceID, EventRecord, Reconciler, and Track B
  B1 evidence surfaces.

## Milestones

- Live queue truth verified.
- Schema/helper/CLI/tests implemented.
- Deterministic reports generated.
- Task evidence written.
- Validation matrix run.
- Task stopped at `needs_review`.

## Verification Intent

Run Python compile checks, focused unit tests, `conformance-result`
status/project/validate, JSON parsing for generated reports, task
inspect/evidence checks, predecessor validators, broad AIDE validation, Git diff
checks, secret-like value scan, and commit policy validation.

## Exit Criteria

The task stops at `needs_review` with `PASS_WITH_WARNINGS`, writes complete
evidence, preserves result/projection-only semantics, binds to the exact accepted
ConformanceProfile candidate, keeps result validity/profile satisfaction separate
from admission, generates the next check prompt, and commits the bounded slice.

## Non-Capabilities

This task does not implement conformance runners, case execution, command
execution, automatic result collection, profile activation, conformance
admission, subject admission, trust grants, adapter admission, adapter execution,
PatchTransaction, AdapterManifest, ContextPack v2, runtime, worker execution,
provider/model/network/Gateway calls, target apply, branch/worktree automation,
release, promotion, production readiness, or broad autonomous runtime behavior.
