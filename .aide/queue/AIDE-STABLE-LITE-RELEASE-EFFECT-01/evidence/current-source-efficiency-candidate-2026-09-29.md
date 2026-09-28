# Current source Lite 1.0.0 local qualification

The prior accepted `42672db9` effect remains historical. The corrected
portable usage parser was independently accepted as source
`46c51f7101c3d4d5018ea8c6b59b132e4bf558a0` and integrated into local
and remote `dev@8912eab9071cd2599fb4f43721aa0dafea807a8e`.
This record covers a superseding **local candidate**, not publication.

The 50-commit changelog preview at `8912eab9` passed validation with zero
malformed messages. Pack source commit `65fafcc9f5bed0a32a5f9aaaa0155a815e0f3599`
passed the D-managed export job `b4c1fc11` and pack-status checksum,
provenance and boundary checks. The postcommit export replay `351f97bd`
changed zero tracked files. Stable asset commit
`8f9bd0748fab588e7e2c80468c29fbb706df2625`, tree
`479fed368aebd073a1cca2beca0e332dd8d87bad`, passed the D-managed
build `f430fd62`, validation `a3f3d587` and postcommit replay
`b5bebb4d`; replay changed zero tracked files.

Exact local stable bytes:

| Asset | SHA-256 |
| --- | --- |
| ZIP | `5bbe1234492c39c4ad26b4d43b2b1fe0193963bf3b4ddb99f108b0405b72c051` |
| tar.gz | `c42617e1a6e4b3ded8dcf036c0ce0a582732a50ffa1bba1b536bd2e70a8223ad` |
| manifest | `b6b2c0b17cb256c9df61928062bd6a5363e05695afb8d5da9d59271e8fcb34a2` |
| delivered CLI | `2a356a5df8a157cef5e22a3bc36b6c1da5ab383c3e76da46bba8ad84a259ded1` |

Six serial delivered-byte consumer jobs passed: fresh
`cafab263`, lifecycle `c3190aa6`, context/offline `75d1cf50`,
partial `c8ecefa0`, public CLI `e530711d` and forced restart
`96bd3a16`. Their ignored local summary is
`.aide.local/final-consumer-new-policy.json`, SHA-256
`9aceee87b1cb5174e311d8109f993b1aad85de7c1cef882df0393b303bb26731`.
It records scratch retirement and reservation release. A fresh disposable
Git consumer observed ten delivered `job` forms with the same ZIP and CLI
hashes. Its ignored local summary is `.aide.local/current-job-forms.json`,
SHA-256 `928c17b579cd8e2fdb4d10d19427a77f73736b0756fa90c5bd4c979b4855d87b`;
its inner fixture source commit is distinct from the AIDE release source.

The current Q47/Q48 D-managed job `c367d2f8` passed all 36 tests in
66.361 seconds, receipt SHA-256
`3828fb837f5be6b8fcdcf91e32573cb0a627823547e5a2afd6f4330f8719c57d`.
The current local preview bundle and draft generation/validation jobs
`8f219e89`, `d3c44897`, `c0cd993d` and `abcab616` all passed.
The bundle and draft remain explicitly local and unpublished.

No live Codex model turn, actual model usage measurement, main promotion,
tag, upload, remote download or arbitrary project rollout was performed.
The current outputs still require postcommit replay, exact technical review
and legitimate integration. Main history still has ten unresolved historical
message decisions. The larger programme remains active.
