# AIDE-BUILD-CONFORMANCE-PROFILE-01 ExecPlan

## Objective

Build the first minimal AIDE `ConformanceProfile` vertical slice for the
accepted `minimal_capability_manifest` capability.

## Scope

- Add `aide-conformance-profile.schema.json`.
- Add `core/protocol/conformance_profile.py`.
- Register `conformance-profile status/project/validate` in `aide_lite.py`.
- Generate deterministic profile, profile index, case index, projection, status,
  validation, future-work, and unfinished-work reports.
- Add focused tests for profile validation, case validation, dependency handling,
  fail-closed rules, CLI dispatch, and no-overclaiming boundaries.
- Materialize queue task metadata and evidence.

## Dependencies

- `AIDE-ACCEPT-CAPABILITY-MANIFEST-01` result:
  `ACCEPTED_WITH_WARNINGS`.
- Existing ReferenceID and EventRecord validation surfaces.
- Track B B1 barrier warning debt remains classified and unrepaired.

## Milestones

- Live queue truth verified.
- Schema/helper/CLI/tests implemented.
- Deterministic reports generated.
- Task evidence written.
- Validation matrix run.
- Task stopped at `needs_review`.

## Verification Intent

Run Python compile checks, focused unit tests, `conformance-profile`
status/project/validate, JSON parsing for generated reports, task
inspect/evidence checks, predecessor validators, broad AIDE validation, Git diff
checks, and commit policy validation.

## Exit Criteria

The task stops at `needs_review` with `PASS_WITH_WARNINGS`, writes complete
evidence, preserves profile-only semantics, generates the next check prompt, and
commits the bounded slice.

## Non-Capabilities

This task does not implement ConformanceResult, conformance execution, admission
policy, adapter admission, adapter execution, PatchTransaction, AdapterManifest,
ContextPack v2, runtime, worker execution, provider/model/network/Gateway calls,
target apply, branch/worktree automation, release, promotion, production
readiness, or broad autonomous runtime behavior.
