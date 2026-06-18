# Next Task Prompt: AIDE-ACCEPT-CONFORMANCE-PROFILE-01

Execute the acceptance gate for the checked minimal ConformanceProfile slice.

## Inputs

- `AIDE-BUILD-CONFORMANCE-PROFILE-01` result: `PASS_WITH_WARNINGS`
- `AIDE-CHECK-CONFORMANCE-PROFILE-01` result: `PASS_WITH_WARNINGS`
- profile_ref: `aide://conformance-profile/minimal_capability_manifest-v1.0.0`
- subject_ref: `aide://capability/minimal_capability_manifest`

## Acceptance Objective

Consolidate build and check evidence and decide whether the candidate
ConformanceProfile should be accepted with warnings as the current profile-only
admission-requirements mechanism for `minimal_capability_manifest`.

## Required Boundaries

Do not implement `ConformanceResult`, conformance runner/execution/admission,
adapter admission/execution, `PatchTransaction`, `AdapterManifest`, ContextPack
v2, runtime, provider/model/network calls, target apply, branch/worktree
automation, release, promotion, or production readiness.

## Expected Next Work

If accepted, recommend `AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-01`.
