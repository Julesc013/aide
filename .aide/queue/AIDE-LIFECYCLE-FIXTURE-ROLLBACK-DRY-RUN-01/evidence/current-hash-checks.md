# Current-Hash Checks

Report: `.aide/reports/lifecycle-fixture-rollback-dry-run/current-hash-checks.json`

Algorithm: `sha256`

Result: `PASS_WITH_WARNINGS`

Concrete fixture files checked:

- `.aide/examples/apply/lifecycle-fixtures/target/existing-managed-section/manual/with-managed-section.md`
- `.aide/examples/apply/lifecycle-fixtures/expected/install-managed-section/manual/with-managed-section.md`
- `.aide/examples/apply/lifecycle-fixtures/target/upgrade-v1-installed/generated/upgrade.md`
- `.aide/examples/apply/lifecycle-fixtures/expected/upgrade-v2/generated/upgrade.md`

Matches:

- `fixture-rollback-install-managed-section` preimage hash matched.
- `fixture-rollback-install-managed-section` postimage hash matched.
- `fixture-rollback-upgrade-v2` preimage hash matched.
- `fixture-rollback-upgrade-v2` postimage hash matched.

Mismatches: none.

Placeholders:

- `lifecycle-rollback-compatible-record-example` is generic example-only and has placeholder preimage/postimage hashes.
