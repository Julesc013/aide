# Validation

- `repo inventory` and `repo status`: PASS.
- `repo validate`: WARN only for four unknown classifications.
- `quality ledger`, `quality status`, and `quality validate`: PASS with advisory warnings.
- `refactor status`, `plan`, `dry-run`, and `validate`: PASS; no apply available.
- `roots inventory`, `classify`, `plan`, and `validate`: PASS; no moves or deletes.
- SHA-256 loose-file and ZIP-member verification: PASS for both compact Facman custody archives.
- Active-lane archive comparison: 506 remaining untracked files matched named
  members of tracked task-owned ZIPs with zero loose or archive mismatches.
- Exact cleanup candidate: 506 files and 101,279,517 bytes.
- Candidate manifest SHA-256:
  `77d6f576f3840971e1b9b470dd809819963662c0ac4c1009dfc5372f72b11029`.

Generated audit reports are advisory and are not canonical source truth.
