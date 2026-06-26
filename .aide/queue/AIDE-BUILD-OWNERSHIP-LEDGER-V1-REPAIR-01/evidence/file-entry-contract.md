# File Entry Contract

OwnershipLedger records now include explicit file-entry fields for entry ref,
target relative path, owner ref, distribution and component refs, installed and
observed digests, portable role, distribution mutability, preservation policy,
operation constraints, platform notes, case-sensitivity notes, deterministic
observation timestamps, and supersession refs.

Validation refuses missing owners, missing vendor source refs, digest mismatch,
distribution mutability, missing evidence refs, unresolved symlink entries, and
unresolved reparse-point entries.

Report matrix:

```text
.aide/reports/ownership-ledger-v1-repair-01/file-entry-contract-matrix.json
```
