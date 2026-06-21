# Conformance Evidence Repair

Conformance results now carry expectation-specific `assertion_id`, `expected`, `observed`, and `evidence_refs` fields. Aggregate-only conformance returns `NOT_PROVEN`; passing conformance requires a bundle plus validation evidence.
