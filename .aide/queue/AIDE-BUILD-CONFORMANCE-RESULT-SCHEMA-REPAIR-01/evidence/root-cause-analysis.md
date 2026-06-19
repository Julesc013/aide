# Root Cause Analysis

The defect was in `core/protocol/conformance_result.py`.

Before repair:

1. `load_accepted_conformance_profile()` loaded the accepted profile report.
2. `_validate_profile_binding()` produced a lifecycle warning for candidate profiles.
3. `load_accepted_conformance_profile()` deep-copied the profile and appended the warning to `status.validation_warnings`.
4. `build_conformance_result()` calculated `profile_digest()` over that mutated copy.
5. `validate_conformance_result()` loaded the profile through the same mutating path and recomputed the same mutated digest.

The result was a false-positive digest validation path. The result digest did
not bind to the pristine accepted profile payload.
