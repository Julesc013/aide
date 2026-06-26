# Q43 Migration

The repair adds deterministic Q43 ownership-class migration as projection-only
behavior. It maps supported Q43 classes into v1 ownership classes, routes
ambiguous unknown ownership to manual review, and refuses unmapped classes with:

```text
ownership.migration_unmapped
```

The AIDE Lite command is:

```text
py -3 .aide/scripts/aide_lite.py ownership-ledger migrate-q43
```

No install state is changed and no target repository mutation is implemented.
