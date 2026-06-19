# Digest Ordering Review

Status: PASS

Digest order after repair:

1. load pristine profile payload
2. validate binding without mutating the profile
3. compute `sha256-canonical-json-v1`
4. build result and case projections
5. validate result against a freshly loaded pristine profile

Validation warnings or lifecycle annotations on a copy do not affect the result
digest.
