# Remaining Risks

- The profile is a candidate and still needs independent review.
- The validator is a local minimal structural validator, not full JSON Schema
  Draft 2020-12 execution.
- The profile defines required checks but does not observe real outcomes.
- `ConformanceResult` is not implemented, so result evidence cannot yet be
  materialized.
- Admission remains a separate future acceptance/policy layer.
- Existing warning debt, including stale generated context projection drift,
  remains intentionally unrepaired.

None of these risks block this build slice because they are the expected
boundaries of `AIDE-BUILD-CONFORMANCE-PROFILE-01`.
