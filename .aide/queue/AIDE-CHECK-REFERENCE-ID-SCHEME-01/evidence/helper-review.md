# Helper Review

Result: PASS_WITH_WARNINGS.

Reviewed helper:

- `core/protocol/reference_id.py`

Findings:

- `parse_reference_id` accepts `aide://<kind>/<id>` references with optional fragments.
- Invalid schemes, missing kinds, missing ids, extra path segments, path traversal, whitespace, and control characters fail closed.
- `format_reference_id` round-trips through the parser.
- `validate_reference_id` warns for unknown optional kinds and fails closed for unknown required kinds.
- `build_reference_record` records stable identity in `spec.ref`, `spec.ref_kind`, `spec.identity`, and `spec.stable_identity`.
- File paths are locators and receive SHA-256 values when the file exists.
- Projection and validation helpers write report files only.

Warnings:

- The helper does not implement runtime resolution, a registry, a resolver service, EventRecord, OKF, PatchTransaction, adapter manifests, or ContextPack v2.
