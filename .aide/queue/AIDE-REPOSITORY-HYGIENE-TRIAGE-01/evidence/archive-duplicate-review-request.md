# Archive-Duplicate Removal Review

## Exact Candidate

- Manifest: `archive-duplicate-candidate.json`
- Canonical committed manifest SHA-256: `381213944009ef69aa4860ccb4269b9a0ecd72091fe3f0cb5fa41de40dcfe47d`
- Pre-index CRLF projection SHA-256: `77d6f576f3840971e1b9b470dd809819963662c0ac4c1009dfc5372f72b11029`
- Candidate files: 506 untracked ordinary files
- Candidate bytes: 101,279,517
- Isolated-host files: 358
- Broker files: 148
- Verification mismatches: 0

Every candidate file has the same SHA-256 as a named member of a tracked
task-owned ZIP. The manifest records the loose path, size, SHA-256, tracked
archive path, and archive member for each file.

Git normalized the generated JSON to LF at the index boundary. Review and
approval bind the canonical committed LF bytes. The CRLF hash is retained only
as a provenance note for the pre-index working-tree projection.

## Proposed Effect

Delete only the 506 exact untracked paths listed in the manifest using
literal-path, non-recursive file removal. Do not delete a directory, tracked
file, archive, custody map, unique evidence record, ignored Facman expansion,
branch, worktree, Git ref, or external recovery file.

Before each removal, recheck that the path is under the current repository,
remains untracked, is an ordinary file, and still matches both the manifest hash
and tracked archive member. Any mismatch fails closed and leaves that path in
place.

## Recovery

The source state is retained in two independent forms:

1. tracked task-owned ZIP archives and custody records; and
2. `D:/Projects/AIDE/_recovery/aide-20260921T0840AEST`.

Restoration can extract the named archive member or use the verified external
snapshot. No Git history rewrite is involved.

## Decision Boundary

Approval of this exact manifest authorizes only the literal untracked-file
removal described above. It does not approve tracked-file deletion, archive
retirement, generated-report pruning, branch deletion, worktree pruning, force
push, main promotion, tagging, release upload, or publication.
