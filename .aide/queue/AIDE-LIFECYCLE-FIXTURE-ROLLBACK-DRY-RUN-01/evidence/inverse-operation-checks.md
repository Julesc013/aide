# Inverse Operation Checks

Report: `.aide/reports/lifecycle-fixture-rollback-dry-run/inverse-operation-checks.json`

Result: `PASS`

Inverse operations checked:

- `restore_managed_section_preimage` for the generic example.
- `restore_managed_section_preimage` for `fixture-rollback-install-managed-section`.
- `restore_file_preimage` for `fixture-rollback-upgrade-v2`.

All checked inverse operations require matching current hash before rollback. No executable rollback code claim is made. Unknown ownership, target truth replacement, and broad delete remain unsupported rollback cases.

Broad delete and broad moves remain blocked. Target repo mutation and active repo scoped apply mutation remain blocked.
