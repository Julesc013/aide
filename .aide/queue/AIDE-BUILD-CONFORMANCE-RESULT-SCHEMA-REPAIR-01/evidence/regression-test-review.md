# Regression Test Review

Status: PASS

Added regression tests:

- `test_profile_digest_matches_pristine_payload_independent_calculation`
- `test_profile_digest_ignores_validation_warning_mutation_of_copy`
- `test_profile_digest_changes_when_pristine_payload_changes`
- `test_projection_and_validation_do_not_mutate_profile_source`

The independent digest test uses `hashlib.sha256` and canonical `json.dumps`
directly rather than calling the production digest helper.
