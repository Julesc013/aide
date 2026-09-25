# Combined rollback and removal source, local artifact projection

## Frozen source and reviews

- Combined source commit `723322cf07abae660d28259d5187cae08e1e2aea`, tree `13d6b42ef3f13c392d1cfb982022db3f8686d89b`, contains rollback source `33824b36` and removal repair `2c4c9089` in ancestry. Both contributing branches received independent bounded source acceptance. The original removal source `d5b44626` was rejected and retained in history; `2c4c9089` repaired its orphaned backup recovery defect.
- Exact combined-source independent verdict: `ACCEPT_WITH_NOTES`, external report `D:/Projects/AIDE/_review_scratch/lifecycle-combined-723322cf-independent-source-review.md`, SHA-256 `b4a7709e85a77e76152e39294a94358695d1111bf351cec334667842be6208b4`. It covers source combination only.
- The pending-removal rollback regression failed before the guard (one test, expected failure) and passed afterward. See `rollback-removal-interaction.md` for exact commands and log digests.
- The combined focused importer command `py -3 -B -m unittest discover -s .aide/scripts/tests -p test_export_import.py -k rollback_refuses_pending_removal -k brownfield_section` passed 9 tests in 295.924 seconds, exit 0; external log `D:/Projects/AIDE/_review_scratch/lifecycle-723322cf-focused.log`, SHA-256 `bc8b4cb4e1d05c3cf850e10cc76661bf227fd166636cd7fe08ba9bf2911491cb`.

## Deterministic local projection from clean source

The source worktree was clean before generation. All commands exited zero in this order:

| Command | External log SHA-256 |
| --- | --- |
| `export-pack --name aide-lite-pack-v0` | `83151ebceb58573bc4f203f7f074c592a537726ef5c308e024f06e6363cb5a0d` |
| `changelog preview` | `545b2af53eddc0511041cb38f16bb0df15310c63966358539639ca638c69b563` |
| `release bundle` | `7f9cf2e5444232635755fa17ed2a5fec059fc8c1ec8be5f97c5cb384e610744e` |
| `release validate` | `8e0f105a0248c91c957c90ebcd1acf09012fa479f088fc3fb3f0fe78f6352a07` |
| `release draft` | `616f59d75a603bcb92e884a4353d3c705e9be30e5b96501b9420a28a9b1a4000` |
| `release draft-validate` | `13103d0bfd1ae6bd60f6e12e9c4d0a9337f3e68b7f599f35c72d82634b8545de` |
| Canonical `validate` | `8f29206e28139058f06530d39e09125c3e12d8a962b4034cb1309e15bf34a8a4` |

Logs are under `D:/Projects/AIDE/_review_scratch/lifecycle-723322cf-<name>.log`. `pack-status` reported `PASS`, zero checksum/provenance/boundary problems. The export contains 828 files and 831 checksum entries; bundle ID is `aide-lite-pack-v0-723322cf07abae66`. Manifest and release provenance both bind `723322cf` and clean source. ZIP SHA-256 `53095e5d7cde55db65c141fdc41c54e787a9e7859b39eca9c2259e9cac7d36b2`; tar.gz SHA-256 `8f42b808b8eedba684a1d0530549adf5c57ee9e0dc3468d5326d46e78fe0b050`.

The wider Q27-Q48 source/fixture suite passed 202 tests in 241.188 unittest seconds, exit 0. External log `D:/Projects/AIDE/_review_scratch/lifecycle-723322cf-release-tests.log`, SHA-256 `d8b5670739eae2019bd9ab7b677a57997d5201aff874cea05cfb33a6215f0034`. `changelog validate`, `changelog status`, and `release status` each exited zero. This is a local preview with `no_publish: true`; it is not a stable-release claim.

## Superseding consumer finding

The preliminary extracted-archive canary independently returned
`REQUEST_CHANGES` for this artifact candidate. Fresh ZIP removal and authored
brownfield tar removal reached `DETACHED`; the v1-to-disposable-v2 update
succeeded. Rollback preview then exited 1 because the receipt's installed
`AGENTS.md` section has authored CRLF line endings while the validated pack
source block has LF line endings. The importer intentionally records distinct
installed and source digests, but the rollback preflight incorrectly required
them to be identical. No later canary scenario ran. The exact report is
`D:/Projects/AIDE/_review_scratch/removal-rollback-combined-consumer-prep/preliminary-723322cf-rollback-crlf-finding.md`,
SHA-256 `bb20b73ba2b6e8772877a1cd71158a1ff4f3f317569bce423add612fa28f7116`.
The incomplete full importer run on this rejected source was stopped after
1239.231 seconds; exit -1, no unittest summary, log SHA-256
`d12726edd44a22f42be386ded2abdec1570e60a7215103d86039e07325c3ca44`.
It is **not** a passing suite result. Exact rejected ZIP/tar/guide/provenance
bytes were copied to external
`D:/Projects/AIDE/_review_scratch/lifecycle-723322cf-rejected-artifacts/`;
archive and guide hashes match those above. Repair this defect with a red/green
Windows regression, then regenerate and requalify new bytes.

## Authored-CRLF rollback source repair

Added `test_rollback_preserves_authored_crlf_agents_and_rejects_changed_section`.
It installs v1 into an authored CRLF `AGENTS.md`, updates a distinct managed
payload to v2, checks the receipt's separate exact source and installed block
digests, previews rollback, tests a direct managed-block edit and a re-digested
forged receipt, then applies exact v2-to-v1 rollback while preserving authored
outside bytes. Against source `723322cf`, the test failed at rollback preview
with the independently observed `baseline differs from current pack: AGENTS.md`
error: one test, exit 1, 33.845 wall seconds, log SHA-256
`b13c5c1f17db8645803eca9b5de444483907aac831c491bfd5ee23d94774daa4`.

The source change retains exact pack source digest and receipt/target equality
checks. For only the managed `AGENTS.md` section it permits the installed
digest of the exact pack block rendered with LF or CRLF, the two newline styles
`merge_agents_text` emits. Other managed files still require byte-identical
installed and source digests. The same new test passed after repair: one test,
exit 0, 52.248 wall seconds, log SHA-256
`6645855fc96aff35a28773d8810505295a85923be03d8f6a62622c13f73e9ba6`.
Both external logs are under `D:/Projects/AIDE/_review_scratch/` with names
`lifecycle-crlf-rollback-red.log` and `lifecycle-crlf-rollback-green.log`.
Python AST and `git diff --check` passed. Wider affected tests, new exact
source review, regenerated artifacts and final consumer canary remain open.
The full rollback-focused importer subset subsequently passed 8 tests in
273.085 unittest seconds (280.647 wall seconds), exit 0, external log
`D:/Projects/AIDE/_review_scratch/lifecycle-crlf-rollback-focused.log`,
SHA-256 `5a393ea0948cb4f4a3dbdd065dc4367411b592e1ab69e705a0d5cb2e2a35de09`.
Superseding source SHA-256 is
`cf7eab84c392a6ae78e9d7df26a354fb43d0929a75ce609fc2f62e33db4cc4e6`;
test SHA-256 is
`ed3d8506ec4784f51cd7fa705b9e77e0429de52a23fde932213aff29166aae2c`.

## Outstanding gates

The superseding source, full importer suite, completed extracted ZIP/tar
lifecycle canary, artifact commit, metadata convergence, final zero-diff replay,
independent artifact/effect review, and observed `dev` integration are pending.
Native, hosted, update-conflict, main and public release gates remain separate.
