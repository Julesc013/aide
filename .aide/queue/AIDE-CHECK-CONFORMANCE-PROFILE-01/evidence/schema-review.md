# Schema Review

Result: `PASS_WITH_WARNINGS`

The schema declares `kind: ConformanceProfile`, profile identity, subject
identity, case records, result/admission/trust false flags, and explicit
profile-only boundaries.

Non-blocking note: the case structure is modeled inline under `spec.cases`
rather than factored into a separate `$defs` block. The required case semantics
remain explicit and are validated by the helper and focused tests.
