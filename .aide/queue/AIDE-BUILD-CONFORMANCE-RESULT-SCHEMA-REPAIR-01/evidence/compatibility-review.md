# Compatibility Review

Status: PASS_WITH_WARNINGS

The repair changes the semantic digest algorithm for the ConformanceResult
profile binding to the explicit `sha256-canonical-json-v1` contract. The result
record remains the same result ref and schema version, and no schema migration
is required because the digest field remains a `sha256:` string.

Warning:

- Existing historical reports retain the prior incorrect digest as evidence.
