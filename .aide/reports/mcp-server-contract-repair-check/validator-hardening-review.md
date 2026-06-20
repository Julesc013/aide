# Validator Hardening Review

Temporary in-memory fixture mutations were injected and validated.

The validator failed closed for:

- `cursor: null`
- numeric `cursor`
- boolean `cursor`
- object `cursor`
- array `cursor`
- `nextCursor: null`
- numeric `nextCursor`
- boolean `nextCursor`
- object `nextCursor`
- array `nextCursor`
- resource-not-found error code `-32043`

Valid opaque string cursor and nextCursor values passed.

Warning: production validator diagnostics identify the fixture and field path
and state the omitted-or-string rule. The independent injected-case evidence
records the observed invalid type for each case; the production diagnostic text
does not print the observed type in every message.
