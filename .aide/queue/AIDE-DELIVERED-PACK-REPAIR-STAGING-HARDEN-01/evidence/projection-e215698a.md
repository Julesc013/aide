# Exact Windows repair staging source and local artifact projection

Source commit `e215698a993d1904152c614ec84b71741f4bb086`, tree
`d0ef0924298171d77d2988873c20c9a8763b0716`, descends from dev
`9a8b08700ef7356ee75b6750f3a53c97a4a56e3e`. No main, tag, upload,
hosted, or public release effect occurred.

The focused Windows repair suite passed 11/11 in 175.772 seconds; log
`D:\Projects\AIDE\_review_scratch\repair-staging-focused-repair-suite-v3.log`
SHA-256 `e45242abc8e3e7bc200fdc3a7defbf0c2f7494e07cd4fb1a94fc80760a74050d`.
The exact source full importer suite passed 44/44 in 617.176 seconds; log
`D:\Projects\AIDE\_review_scratch\repair-staging-full-importer-suite-v2.log`
SHA-256 `a16d47bf4e23c36d577783226e5209d6ab91500cdb57455f8ebeabecd86c1788`.

Independent reviewer `/root/owned_repair_integration_review` returned
ACCEPT_WITH_NOTES for **dev source integration only** on the exact commit/tree.
The unchanged external original is
`D:\Projects\AIDE\_review_scratch\repair-staging-e215698a-independent-review.md`,
SHA-256 `9f56c005d4d8c8f026e49ee5d063c047d2f2ea66a3cf3cdd20037c69e5952001`.
A simulated cleanup failure after successful link leaves expected destination
bytes and a residual stage; this is an uncertain recovery effect, not
no-effect/replay authority. The first source `1a44ec61` and its 43/43 full
suite are historical and do not replace the superseding 44/44 result.

From clean `e215698a`, `export-pack`, `changelog preview`, `release bundle`,
`release validate`, `release draft`, and `release draft-validate` all exited
zero. The export manifest and release provenance both bind full source
`e215698a` with `source_dirty_state: false` / `dirty_state: false`.
The local bundle ID is `aide-lite-pack-v0-e215698a993d1904`.
ZIP SHA-256 `949cfc24ac261f2db520e8c1c4e80f46d9f9ac569ae6c6d5ea62c6e0c31434ec`;
tar.gz SHA-256 `26081af25c94d8494542b120ce1adee4df27710e089f65f707daecf8db679c2f`.
The pack reports 828 included files and 831 checksum entries, with boundary
PASS and no provider/model/network calls. `pack-status` reports provenance,
checksums, and boundary PASS. `changelog validate` and `changelog status`
passed as preview-only checks.

The release-adjacent Q47 (18), Q48 (11), Q31 (6), and Q34 (11) tests passed
on ancestor source `1a44ec61` before the narrow setup-failure cleanup change.
They are historical, not exact-source test results; exact-source full importer,
generator and validation results above cover changed repair behavior and
current artifacts. Recheck any affected suite if combined source changes.

Extracted consumers, independent artifact verdict, postcommit zero-change
replay, and dev integration are pending at this checkpoint.
