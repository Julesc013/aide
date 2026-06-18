# Helper Review

Result: `PASS`

`core/protocol/conformance_profile.py` defines deterministic profile
construction, known evaluators, explicit non-capabilities, forbidden-claim
patterns, validation checks, and report projection helpers.

The helper keeps unknown required evaluators fail-closed and keeps unknown
optional/advisory evaluators warning-only.
