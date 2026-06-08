# Hash Reference Checks

Result: `PASS`

Algorithm: `sha256`

Checked hashes:

- `upgrade-v2` preimage `generated/upgrade.md`: match.
- `upgrade-v2` postimage `generated/upgrade.md`: match.
- `upgrade-manual-preserved` preimage `manual/with-managed-section.md`: match.
- `upgrade-manual-preserved` postimage `manual/with-managed-section.md`: match.
- `drift-detected` preimage `manual/with-managed-section.md`: match.

No placeholder hashes were found. No future-computed hash fields were required by the upgrade scenarios checked here.

Detailed machine-readable evidence:

- `.aide/reports/lifecycle-fixture-upgrade-dry-run/upgrade-hash-reference-checks.json`
