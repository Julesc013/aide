# Helper Review

Helper: `core/protocol/reference_id.py`.

Checked behavior:

- `parse_reference_id` accepts stable `aide://<kind>/<id>` references with optional fragments.
- Invalid schemes, missing kinds, missing ids, path traversal, extra path segments, whitespace, and control characters fail closed.
- Unknown optional ref kinds warn.
- Unknown required ref kinds fail closed.
- `build_reference_record` keeps stable identity in `spec.ref` and `spec.identity`.
- File paths remain locators and include SHA-256 hashes when the locator exists.
- Explicit non-capabilities are embedded in every projected ReferenceID record.

Boundary:

- The helper writes reports and reference maps only. It does not implement runtime lookup, service state, registry mutation, leases, schedulers, provider calls, target mutations, or branch/worktree operations.
