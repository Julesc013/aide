# Tracked Output Retention Assessment

## Current Inventory

- Tracked files: 11,113.
- Tracked working-tree bytes: 103,853,570.
- Tracked `.aide/` files: 10,439.
- Tracked `.aide/` bytes: 98,408,940.
- Live `specs/` files: 66.
- Live `specs/` bytes: 400,369.

The dominant tracked bulk remains generated output and evidence, not the live
specification tree.

## Generated-Output Ledger

The tracked generated-output ledger contains 1,381 entries:

- exported copies: 818;
- generated reports: 470;
- projections: 54;
- tool-specific projections: 24;
- generated context: 12;
- unknown candidates: 3.

All 1,381 entries currently report both `safe_to_delete: unknown` and
`safe_to_regenerate: unknown`. Only 14 generators are marked known; 1,300 are
inferred and 67 are unknown. The ledger therefore does not support tracked-file
deletion yet.

The largest tracked generated views include:

- `.aide/repo/dependency-map.json`: 10,537,261 bytes;
- `.aide/reports/file-quality-ledger.json`: 5,528,827 bytes;
- `.aide/repo/doc-link-map.json`: 4,349,906 bytes;
- `.aide/roots/latest-root-classification.json`: 4,334,394 bytes;
- `.aide/repo/file-inventory.json`: 3,469,938 bytes;
- `.aide/ledgers/generated-output.yaml`: 2,334,849 bytes.

## Retention Decision

Retain tracked generated outputs and custody archives in this task. Size, age,
`latest-*` naming, generated classification, duplication, or orphan candidacy
does not prove safe deletion.

A future migration may untrack a generated family only after it records:

1. its canonical source records and exact generation command;
2. deterministic regeneration from a clean checkout;
3. consumer and documentation references;
4. required historical or release evidence retention;
5. a replacement location such as ignored local state or CI artifacts;
6. an exact removal manifest and rollback/recovery procedure.

## Local And Git Caches

- Remaining ignored files: 184 totaling 4,648,399 bytes; these are retained task
  evidence, not classified cache.
- Remaining `__pycache__` directories: zero.
- Registered worktrees: one live worktree.
- Git object-store garbage: zero bytes.
- Git garbage collection or object pruning: not justified and not run.
- Machine-wide Codex/plugin caches: retained because they are active extension
  dependencies and were outside this repository-cleanup scope.
