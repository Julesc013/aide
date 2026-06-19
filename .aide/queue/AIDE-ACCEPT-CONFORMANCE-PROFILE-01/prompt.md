# Prompt: AIDE-ACCEPT-CONFORMANCE-PROFILE-01

Accept the completed ConformanceProfile build/check chain as
`minimal_conformance_profile`.

## Inputs

- `AIDE-ACCEPT-CAPABILITY-MANIFEST-01`: `ACCEPTED_WITH_WARNINGS`
- `AIDE-BUILD-CONFORMANCE-PROFILE-01`: `PASS_WITH_WARNINGS`
- `AIDE-CHECK-CONFORMANCE-PROFILE-01`: `PASS_WITH_WARNINGS`
- profile_ref: `aide://conformance-profile/minimal_capability_manifest-v1.0.0`
- subject_ref: `aide://capability/minimal_capability_manifest`

## Acceptance Boundary

Accept only the protocol capability to represent, project, validate, version,
and inspect candidate ConformanceProfile objects.

Do not activate the candidate profile, generate ConformanceResult, execute
cases, perform admission, admit `minimal_capability_manifest` by conformance,
grant trust, admit adapters, run workers, or introduce runtime behavior.

## Expected Result

`ACCEPTED_WITH_WARNINGS`, stopped at `needs_review`.

## Next Task

`AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-01`
