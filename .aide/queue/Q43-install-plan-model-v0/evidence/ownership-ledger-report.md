# Ownership Ledger Report

## Schema

- `.aide/install/ownership-ledger.schema.json`
- `.aide/install/ownership-record.schema.json`

## Latest Example

- path: `.aide/install/latest-ownership-ledger.example.json`
- records: 464
- no_apply: true

## Ownership Classes

The ledger supports:

- installed_file
- managed_section
- generated_target_artifact
- preserved_target_artifact
- external_manual_artifact
- local_only_artifact
- source_pack_artifact
- unknown

## Future Use

Future install, repair, upgrade, rollback, and uninstall phases can use this ledger to distinguish source-pack files from target-specific files. Q43 does not apply ownership changes.
