# Repair Scenario Review Evidence

Result: `PASS_WITH_WARNINGS`

Independent consistency check output:

```text
PASS repair dry-run independent consistency check
scenarios=2 expected_report_refs_present=0 hash_matches=2 marker_checks=2 no_apply=true
```

Scenario conclusions:

- `repair-plan-missing-marker`: `BLOCKED` by `BLOCKED_MARKER_MISSING`; path, marker, hash, and mutation checks pass.
- `repair-plan-malformed-marker`: `BLOCKED` by `BLOCKED_MARKER_MALFORMED`; path, marker, hash, and mutation checks pass.

Both generated plans are fixture-only, use `mode=report`, require explicit path `manual/with-managed-section.md`, preserve protected roots, require SHA-256 preimage hashes, stop at `needs_review`, and prohibit apply execution and target mutation.
