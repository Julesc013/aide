# Hash Reference Checks

Report: `.aide/reports/lifecycle-fixture-repair-dry-run/repair-hash-reference-checks.json`

Result: `PASS`

Algorithm: `sha256`

Files checked: 2

Hash matches: 2

Hash mismatches: 0

Checks:

- `repair-plan-missing-marker`: `.aide/examples/apply/lifecycle-fixtures/target/missing-marker/manual/with-managed-section.md` matched `sha256:cdbda48c7ab0f5eea8690ce5e58a2c006197bb343f6599b82b1a73bb1953fca0`.
- `repair-plan-malformed-marker`: `.aide/examples/apply/lifecycle-fixtures/target/malformed-marker/manual/with-managed-section.md` matched `sha256:c27b23ce54154d00ecddacb4bd10fc66fd1a52cf4c129749ecbc52d11a5f56b5`.

Postimage hashes required: 0, because both scenarios are expected blocked marker-defect cases.

Placeholders found: none.

Future-computed fields: none.
