# Combined historical source and artifact validation

Source merge commit `e40aec47dd2dd5555d00f869262c3fb000a2e617`
has tree `ca5fc9421612300299747249e6d76148f36ef5d6` and exact parents
`a5cd5ca5ddf7d0be561fbf2796b073b9f5d96fd2` (accepted customization
dev) and `7a2305f518940077892729b915734bb766a335e1` (published
historical decisions). No older branch generated pack or release file was
used in its tree. The current dev generator was run from this committed
combined source.

| Check | Result |
| --- | --- |
| Historical commit recovery tests | 23/23 PASS |
| Combined export/import tests | 29/29 PASS in 362.467 seconds |
| Local release bundle tests | 18/18 PASS in 34.512 seconds |
| Local draft tests | 11/11 PASS in 15.898 seconds |
| Portable governance tests | 6/6 PASS in 44.870 seconds |
| Changelog preview | PASS; latest 50 commits, zero malformed |
| Portable export | PASS; 828 files, 831 checksums; source registry excluded |
| Pack status | PASS provenance, checksums, and boundary |
| Local release bundle and draft | PASS, preview only, no tag/upload/publication |
| Changelog/release/draft validation | PASS |
| Canonical validate and doctor | Exit 0 |
| Repeated generation | 888 files compared, zero byte changes on the stable replay |

The first local bundle attempt failed because the changelog preview still
named the previous source. Regenerating the preview for `e40aec47` resolved
that stale projection. A later full generation pass changed bytes from the
earlier order; another complete pass then changed zero of 888 files. The
stable replay comparison used a per-file SHA-256 map stored externally at
`D:\Projects\AIDE\_review_scratch\historical-dev-replay-hashes-before.json`.
The matching map has 888 paths. This is pre-artifact-commit replay; a second
post-commit replay is still required.

The portable export's `aide_lite.py` SHA-256 equals the combined source file:
`f63be218844ab704674821d8e37d6ca5b04502ffb957fcf1f5b477799fb0bccf`.
The source-specific `.aide/git/commit-message-dispositions.json` is absent
from the export. Current generated ZIP SHA-256 is
`298b4e7b38c125540a6b04c6405712ca665b895ae64d0fa3fc95ef3a51d59204`;
tar.gz SHA-256 is
`d5a755716cd862147fd7d13a09113493800933c4b0c5487c8a52f8ef28f791f1`.

All logs are external under `D:\Projects\AIDE\_review_scratch\` with
`historical-dev-` prefixes. These are local source and artifact checks,
not native/hosted qualification, stable publication, or downloaded consumer
proof. The historical mechanism and date delta have independent reviews;
the exact combined integration candidate still requires its own review.
