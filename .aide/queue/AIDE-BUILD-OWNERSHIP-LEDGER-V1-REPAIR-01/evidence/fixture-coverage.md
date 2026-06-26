# Fixture Coverage

The fixture corpus now includes:

- direct valid fixtures for all ownership classes;
- a managed-section manual-outside preservation fixture;
- direct invalid fixtures for file-entry, managed-section, Q43, path, case,
  conflict, evidence, symlink, reparse-point, and source mismatch behavior;
- Q43 supported, manual-review, and unmapped migration fixtures.

Fixture validation passes through:

```text
py -3 .aide/scripts/aide_lite.py ownership-ledger validate
```
