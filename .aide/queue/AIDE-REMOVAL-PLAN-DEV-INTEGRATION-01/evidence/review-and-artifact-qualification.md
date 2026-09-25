# Exact combined removal-planner review and artifact qualification

## Frozen subject and ancestry

- Source merge: `1a25e33effc5c8f32311da8cebdd6855ff3185cf`, parents
  `7bc4c9b5087bfdb09b06c6b6cb62ff0707e98878` and
  `d1362f912c951ccc6022d0a2a3a527a4d66365f1`.
- Artifact projection: `9c284081fc33c9f2784479fe1874e58ca2cc489b`.
- Reviewed provenance candidate: `2819385a5b3d6817fbcd45ee9dcc7065b90fbb2c`,
  tree `b57bdab7c47512518d39c91259111878ee7d858b`.
- Current dev parent `1c75abf1d93b34be8998383ea2ce4c9084c9d612` and
  old source `d1362f91` are both ancestors. The old generated artifacts were
  excluded from the source merge.

## Actual independent review

The fresh GPT-6 Sol agent `/root/removal_integration_review` reviewed the
frozen commit/tree read-only and returned **ACCEPT_WITH_NOTES for dev
integration only**. It checked ancestry, read-only planner and receipt/path
checks, generated source provenance, archive hashes, test logs, and extracted
consumers. It noted that the status next action was stale; this evidence-only
closeout fixes that. The self-digested receipt is local ownership evidence,
not authentication: future removal apply needs a separately reviewed effect
path and effect-time revalidation. The review did not accept deletion, native
or hosted operation, real target deployment, main promotion, or publication.
This is a fresh review, not a recovered prior verdict.

## Delivered local bytes and consumers

- ZIP SHA-256: `467b721bf03d8af4d035856334076ff74723a6d1a99a187d5dfba80ed8f5cad3`.
- tar.gz SHA-256: `b7ee412488817528276a3b77e3edcc6bf26c337129b0043027ccd0a8aaceb1b0`.
- Independently rehashed 831 portable pack and 7 release checksum entries:
  zero mismatches. ZIP and tar.gz each have the same 833 safe file names and
  byte hashes. ZIP extraction reported 833 entries.
- Fresh extracted ZIP consumer: safe dry-run planned 816 operations with zero
  conflicts; exact-preview apply wrote 816; receipt-backed removal plan found
  811 candidates, zero preserved, and changed zero of 817 target files. Target
  tree digest before/after: `7b0d93287c1702385176a00e673b9752ad6246591129a690656a291afa0546c4`.
- Brownfield extracted ZIP consumer: authored `AGENTS.md`, project state, and
  notes were present before import; exact-preview apply wrote 815. A direct
  edit to a managed prompt then yielded `PRESERVATION_REQUIRED`, 810 future
  candidates and one preserved. The planner returned exit 2 as specified and
  changed zero of 818 target files. Target tree digest before/after:
  `daaa28e4c9c2e4cfdc4af97885a31ae86f4cbe1cc2f75ebbf6a0831ac2c2a9e7`.
  Authored AGENTS text remained present; project state and notes retained their
  original SHA-256 digests.
- Consumer originals remain under
  `D:/Projects/AIDE/_review_scratch/removal-consumer-1a25e33e/`. The fresh
  apply log SHA-256 is `db1ba636d7bb93bde241620fa5d1fc69f1093a4f4023996a0f9908d1c32a94fb`;
  brownfield plan JSON SHA-256 is
  `055d6daed33ff2f44ea2c3bb98ddc0f89ea594e0487dcd630b8e77aaf1728c0d`.

## Post-commit replay

From clean `2819385a`, `release bundle`, `release validate`, `release draft`,
and `release draft-validate` all passed. The 44 tracked release files had
aggregate digest `318778a60d1233d9d5e0cec1ffe1825f607f9eebd103fadc4b2a867a003461db`
before and after; `git status --short` remained empty. `pack-status` reported
`PASS_SOURCE_ANCESTOR`. All local release/draft outputs still say no-publish.

## Retained gates

This qualifies read-only removal planning for dev source integration. Actual
uninstall deletion, native/hosted effects, stable publication, and downloaded
asset acceptance remain unfinished campaign work.
