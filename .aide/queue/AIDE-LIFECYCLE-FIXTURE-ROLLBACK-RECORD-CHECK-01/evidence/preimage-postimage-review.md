# Preimage / Postimage Review

Result: `PASS`

Algorithm: `sha256`

Concrete files checked: 4

- Install preimage: `.aide/examples/apply/lifecycle-fixtures/target/existing-managed-section/manual/with-managed-section.md`
- Install postimage: `.aide/examples/apply/lifecycle-fixtures/expected/install-managed-section/manual/with-managed-section.md`
- Upgrade preimage: `.aide/examples/apply/lifecycle-fixtures/target/upgrade-v1-installed/generated/upgrade.md`
- Upgrade postimage: `.aide/examples/apply/lifecycle-fixtures/expected/upgrade-v2/generated/upgrade.md`

Hash matches: 4

Hash mismatches: 0

Placeholder result: PASS for fixture records; the generic schema example intentionally uses example placeholder hash text and is not treated as concrete fixture evidence.

Future-computed result: PASS; fixture records use concrete hashes, not future-computed placeholders.

Snapshot/content-reference result: PASS. Fixture record content references exist and match hashes.

Defects: none.
