# Conflict Model

The repair adds validation for:

- duplicate target paths;
- case-fold target-path collisions;
- file-section authority conflicts;
- managed-section overlaps;
- nested managed sections without explicit precedence;
- missing evidence references;
- source distribution/component mismatches;
- unresolved symlink entries;
- unresolved reparse-point entries.

Report matrix:

```text
.aide/reports/ownership-ledger-v1-repair-01/conflict-model-matrix.json
```
