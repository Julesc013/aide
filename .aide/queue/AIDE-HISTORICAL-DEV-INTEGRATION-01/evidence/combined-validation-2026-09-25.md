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
The matching map has 888 paths. That projection was committed at
`3326868b534d6a514af14c4ca3aabc9dc8230579`. A post-commit check then
correctly exposed `DIRTY_SOURCE_RECORDED`: its pack export had run after
generated preview files dirtied the working tree. The projection was
superseded locally by running export **first from clean commit `3326868b`**,
then changelog preview, release bundle, and draft. The corrected manifest
records `source_commit: 3326868b534d6a514af14c4ca3aabc9dc8230579` and
`source_dirty_state: false`; pack-status, release validate, and draft-validate
all pass. A clean-provenance replay of preview, bundle, and draft compared
all 888 generated files and changed zero; its tree digest before and after
was `7722774616539b12707707f59589a3c196a559dd671d78b114eaf1e69a28b9a0`.
The clean-provenance projection was committed in the exact integration
candidate `7c12fc4013847531726c07a3064300d08c637e29` (tree
`f579b2da285752a4231777a58d36c696f788870d`). Its post-commit
release bundle, validate, draft, and draft-validate replay passed and changed
zero of 44 release files. Pack status is `PASS_SOURCE_ANCESTOR`; the export
source commit is the clean ancestor `3326868b534d6a514af14c4ca3aabc9dc8230579`.
The earlier 888-file result describes deterministic bytes for the
superseded dirty-provenance projection, not final clean provenance.

The portable export's `aide_lite.py` SHA-256 equals the combined source file:
`f63be218844ab704674821d8e37d6ca5b04502ffb957fcf1f5b477799fb0bccf`.
The source-specific `.aide/git/commit-message-dispositions.json` is absent
from the export. Corrected clean-provenance ZIP SHA-256 is
`1c797d61f5c559b1e3424c71dc7306095e3438e2184351a3e02ff464c4b43fd8`;
tar.gz SHA-256 is
`b2d4dc7d5ef52c0bad0394bb6cf80d14dc1fa09ea7f93147c51d03f6473588f6`.

All logs are external under `D:\Projects\AIDE\_review_scratch\` with
`historical-dev-` prefixes. These are local source and artifact checks,
not native/hosted qualification, stable publication, or downloaded consumer
proof. The historical mechanism and date delta have independent reviews;
The exact combined candidate received an independent `ACCEPT_WITH_NOTES`
source/artifact verdict. The reviewer required this separate evidence-only
closeout and a narrow check before the dev fast-forward. See
`review-and-consumer-closeout-2026-09-25.md`; native, hosted, main, and
publication acceptance remain open.
