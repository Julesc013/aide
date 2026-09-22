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
- Canonical committed manifest SHA-256:
  `381213944009ef69aa4860ccb4269b9a0ecd72091fe3f0cb5fa41de40dcfe47d`.
- Pre-index CRLF projection SHA-256:
  `77d6f576f3840971e1b9b470dd809819963662c0ac4c1009dfc5372f72b11029`.
- Approved apply: PASS for 506 files and 101,279,517 bytes.
- Post-apply candidate paths remaining: zero.
- Tracked custody archives retained: 20 of 20.
- External recovery snapshot remains present.
- Clean-tree AIDE Git helper plan: `ready_dry_run`.
- Stale worktree metadata prune: PASS; 10 refs and 4 local branches unchanged.
- Detached worktree commit remained readable and reachable from current `HEAD`.
- Python cache dry run and apply: PASS for 20 directories, 69 files, and 1,351,417 bytes.
- Remaining Python cache directories: zero.
- Git object-store garbage: zero bytes; no Git object prune was run.
- Tracked generated-output ledger: 1,381 entries retained because deletion and regeneration safety are unknown for every entry.

Generated audit reports are advisory and are not canonical source truth.
