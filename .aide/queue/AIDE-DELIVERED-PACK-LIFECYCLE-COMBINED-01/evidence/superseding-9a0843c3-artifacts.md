# Superseding combined lifecycle source and local artifacts

## Exact source and retained finding

Source commit `9a0843c3a7633002f91a0ec3e707fe613650eb5f`, tree
`74910425e217869647b72b6595cc5e093d9dc7e0`, parent rejected local
consumer candidate `723322cf07abae660d28259d5187cae08e1e2aea`. The
earlier preliminary ZIP/tar consumer `REQUEST_CHANGES` and exact failed bytes
remain in `combined-source-and-projection.md` and external scratch evidence.

The new source accepts only LF or CRLF rendering of the same validated pack
managed `AGENTS.md` block during exact predecessor rollback. The new Windows
regression failed on the old source, passed on this source, and the rollback
subset passed 8/8. Independent exact delta review returned **ACCEPT for source
only**: external
`D:/Projects/AIDE/_review_scratch/lifecycle-9a0843c3-independent-source-delta-review.md`,
SHA-256 `59ee1b26672c169f764abaf43c19d30e90743f56a936526502e6d12b22e384cb`.
The reviewer independently reran the regression and previewed rollback against
the exact earlier failing disposable target; that read-only preview was
`PLANNED` without changing its receipt or authored `AGENTS.md` bytes. The
report contains those command and log bindings. Artifact/consumer acceptance
is separate.

## Regenerated local output from clean source

The worktree was clean at source `9a0843c3` before regeneration. All six
generator commands returned exit 0 in order:

| Command | External log SHA-256 |
| --- | --- |
| `export-pack --name aide-lite-pack-v0` | `83151ebceb58573bc4f203f7f074c592a537726ef5c308e024f06e6363cb5a0d` |
| `changelog preview` | `335fd8dab6c2add5ac1e1f39c2bd123fb682b06a7ced5041c190246065aedbe4` |
| `release bundle` | `416bc3dac0dfdf61f23eaee9b1a6fd3b285c63c13dea4ae1d0434f2746a3aeb5` |
| `release validate` | `8e0f105a0248c91c957c90ebcd1acf09012fa479f088fc3fb3f0fe78f6352a07` |
| `release draft` | `7d44076e48c3ebb3664c77a2905597d3f0946c7798a3a03d04db33d65e4c58a7` |
| `release draft-validate` | `13103d0bfd1ae6bd60f6e12e9c4d0a9337f3e68b7f599f35c72d82634b8545de` |

Each log is at `D:/Projects/AIDE/_review_scratch/lifecycle-9a0843c3-<name>.log`.
The export includes 828 files and 831 checksum entries. Bundle ID is
`aide-lite-pack-v0-9a0843c3a7633002`. The ZIP SHA-256 is
`d1eaf1bcb7272492b0a4dacf8cd2e291a54471a1051cae002d24c08bb8fb5f00`;
tar.gz SHA-256 is
`ce3066076029d7f0e63172840f838ae4cfd141ae041760663800e72f4b0b218e`;
release `install.md` SHA-256 is
`95a75c1019c749ae3f5e0a213afa4bb01bbe903688e3b78824a79ab258d49c0e`.
`pack-status` reports `PASS`, zero checksum, provenance or boundary problems.
Canonical `validate` exited zero, external log SHA-256
`8f29206e28139058f06530d39e09125c3e12d8a962b4034cb1309e15bf34a8a4`.
`doctor` also exited zero, external log SHA-256
`b1c166c972ad4f4547355783e78c64fa7f9cfecc6837ffdd22e290797b262135`.
The current 44 tracked `.aide/release` files were hashed before any artifact
projection commit. External sorted path/hash list
`D:/Projects/AIDE/_review_scratch/lifecycle-9a0843c3-release-44-before.txt`
has SHA-256 `4258a34ef0300f2010b6b500380878d4393efb73e3e2418e8f6048a33ada938d`.

Affected Q31/Q34/Q47/Q48 suites passed 6/11/18/11 tests, respectively, exit
0. Their external log SHA-256 values are
`845a18ae01e1118cb295707f193a2951819f67561def8f33fd14b0cffe4d85bb`,
`beb99ab6c424392895cd06abd613dcec2f7d85d0ab5aa85673bb1a85054875bb`,
`6ffb22ad6604a0fc0e28dd777b8423ce4d9d663fa2c3626d2d098269086e6e45`,
and `5854ef84fcdf287635083566f73fd268a29f626bb3d35bf79cbf462d318dfa25`.
The complete `test_export_import.py` suite passed **85/85** in 1638.314
unittest seconds (1646.353 wall seconds), exit 0, on frozen source `9a0843c3`
and its current local generated outputs. External log
`D:/Projects/AIDE/_review_scratch/lifecycle-9a0843c3-import-full.log`, SHA-256
`2527f18e86942d957e80ca2d1c97f575cac412ac4498b54b802675c54b7f5322`.

## Independent extracted consumer acceptance

An independent reviewer returned **ACCEPT_WITH_NOTES** for these exact local
ZIP/tar/guide bytes. Report:
`D:/Projects/AIDE/_review_scratch/lifecycle-9a0843c3-independent-consumer-review.md`,
SHA-256 `2f84f1b71f1d0e3a73d601429dd4a7df69169eee161802e6723ce56db1d28085`.
Its external canary script SHA-256 was
`3f3140807520b1481181c34e95e06273e2774698cf2d384e42b5b6214f58a181`.
It exited zero with 49 delivered CLI commands and 833 matching safe ZIP/tar
members. The reviewer independently rehashed all 49 command logs and checked
their expected exit codes: 40 zero, two one, two two and five three. Invocation
log SHA-256 `43fda5934086e09e6e04c734252494a3e9a18236b3205bd297e29eeeb1a70795`;
summary SHA-256 `2fca0b1187763633131230ac413071333eb4398a3ed0b1f7664bb76a1db4331f`;
direct-results SHA-256
`96598c31e0d6008fa46c69ffbc939e0c71e6eed906a23c37e6b455cd421d3071`.
All are under external
`D:/Projects/AIDE/_review_scratch/removal-rollback-combined-consumer-prep/`.

Fresh and authored brownfield targets both fully detached while preserving
unknown and authored bytes. Exact v1-to-disposable-v2-to-v1 rollback returned
`ROLLED_BACK` with CRLF guidance preserved. Stale and fresh conflicts refused
direct edits, pending removal blocked rollback, authored backup failure
reconciled before detach, effect-time changes survived, and interrupted
deletion/receipt retirement recovered. The synthetic v2 is a disposable test
oracle, not a prior public AIDE release; this run does not qualify OS-level
network isolation, native/hosted effects, main or publication. The original
archive and guide hashes stayed fixed through the run.

This remains a local, `no_publish: true` preview. At this consumer checkpoint,
artifact projection, metadata convergence, zero-diff replay, independent
artifact/dev-effect review and observed remote `dev` were pending. Main, tag,
publication, native, hosted and remaining mandatory product obligations are
not accepted by this checkpoint.

## Artifact projection and first postcommit replay

Artifact projection commit `db76505363753fae6fa6d4aeb44ffc2b3c471582`,
tree `8ba90b9b37def925b1d010ceac1c5f53ba7901b5`, records the exact
generated pack, local release files, and the 85-test and 49-command evidence
above. Its commit-message check passed before and after commit. Source remains
frozen at ancestor `9a0843c3`.

The first postcommit `release bundle`, `release validate`, `release draft`,
`release draft-validate` replay all exited zero. External logs in
`D:/Projects/AIDE/_review_scratch/` named
`lifecycle-9a0843c3-postprojection-<command>.log` have SHA-256 values,
respectively, `416bc3dac0dfdf61f23eaee9b1a6fd3b285c63c13dea4ae1d0434f2746a3aeb5`,
`c30eb7108e7489ec43f1f401bf9c07f08a111c52ddac098830e65daf5910e770`,
`7d44076e48c3ebb3664c77a2905597d3f0946c7798a3a03d04db33d65e4c58a7`,
and `13103d0bfd1ae6bd60f6e12e9c4d0a9337f3e68b7f599f35c72d82634b8545de`.
`pack-status` is now `PASS_SOURCE_ANCESTOR` with zero problems and
`release status` reports validation `PASS`, `no_publish: true`.

The replay changed 20 tracked `.aide/release` metadata or draft paths because
the pack source is now a clean ancestor. The release guide changed only its
`pack_status` line from `PASS` to `PASS_SOURCE_ANCESTOR`; its new SHA-256 is
`4ce8b603deff3f817f4b1ad0c58294c6e80b6626c3bd64e343671df6f7bdb977`.
The ZIP SHA-256 remains `d1eaf1bcb7272492b0a4dacf8cd2e291a54471a1051cae002d24c08bb8fb5f00`
and tar.gz SHA-256 remains
`ce3066076029d7f0e63172840f838ae4cfd141ae041760663800e72f4b0b218e`.
The 20 changed metadata paths require a separate convergence commit and a
zero-diff replay from clean HEAD before dev-effect review.
