# Validation

- `repo inventory` and `repo status`: PASS.
- `repo validate`: WARN only for four unknown classifications.
- `quality ledger`, `quality status`, and `quality validate`: PASS with advisory warnings.
- `refactor status`, `plan`, `dry-run`, and `validate`: PASS; no apply available.
- `roots inventory`, `classify`, `plan`, and `validate`: PASS; no moves or deletes.
- SHA-256 loose-file and ZIP-member verification: PASS for both compact Facman custody archives.

Generated audit reports are advisory and are not canonical source truth.
