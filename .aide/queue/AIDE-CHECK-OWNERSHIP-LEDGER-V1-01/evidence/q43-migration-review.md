# Q43 Migration Review

The check oracle requires deterministic Q43 ownership-class migration and an
`ownership-ledger migrate-q43` validation surface.

Observed:

- `py -3 .aide/scripts/aide_lite.py ownership-ledger migrate-q43` exits through
  argparse because valid subcommands are only `status`, `project`, and
  `validate`.
- No Q43 migration helper or fixture corpus is present in
  `core/protocol/ownership_ledger.py`.
- No unmapped-class refusal such as `ownership.migration_unmapped` is emitted.

Disposition: material finding `ownership.q43_migration_missing`.
