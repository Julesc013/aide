# Helper Review

Result: PASS_WITH_WARNINGS.

Reviewed helper:

- `core/protocol/reference_id.py`

Findings:

- `parse_reference_id` accepts `aide://<kind>/<id>` with optional fragments.
- Invalid schemes, missing kinds, missing ids, extra path segments, traversal ids, whitespace, and control characters fail closed.
- `format_reference_id` round-trips through the parser.
- `validate_reference_id` warns for unknown optional ref kinds and fails closed for unknown required ref kinds.
- `build_reference_record` records stable identity in `spec.ref`, `spec.ref_kind`, `spec.identity`, and `spec.stable_identity`.
- File paths are recorded as locators, not identity.
- Existing locator files receive SHA-256 metadata.
- Records embed `explicit_non_capabilities`.
- Projection and validation helpers write reports only.

Warnings:

- The helper is syntactic/projection-only.
- No runtime registry, resolver service, EventRecord, OKF, PatchTransaction, adapter manifest, ContextPack v2, database state, leases, scheduler, supervisor, provider calls, target mutation, branch mutation, network, Gateway, GitHub, or model/provider calls are implemented.

Disposition:

- Non-blocking for acceptance.
