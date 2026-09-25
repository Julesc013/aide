# Combined update and repair-health qualification

2026-09-25. This is local source and artifact evidence for a proposed `dev`
integration, not stable-release or publication acceptance.

## Frozen source and technical review

- Combined source merge `99a9e54da887a3a209cfd73df345c55735819368`,
  tree `7a3838f027031522cb3862815bf15072fd8b538c`, is a descendant of
  `dev@d4b67c96ff81eb10aeecd6763b538331844619c9`. The importer SHA-256
  is `163d8e38bb3ad1f2d8ca2c29c9a946b733b1246c5bf55dfac647b7b693796b57`.
- Independent exact combined-source `ACCEPT_WITH_NOTES`:
  `D:/Projects/AIDE/_review_scratch/update-repair-health-99a9e54d-independent-combined-source-review.md`,
  SHA-256 `2a5408e30bc8d695761a4e5e0467ae73de4190912faf27f494498743aae6cd07`.
  Its notes leave the full suite, artifacts, consumer and `dev` effect as
  separate checks; no changed importer source followed this review.
- Full exact importer suite `py -3 -u -B -m unittest discover -s
  .aide/scripts/tests -p test_export_import.py -v`: exit 0, **100/100 PASS**,
  2384.659 seconds. External log
  `D:/Projects/AIDE/_review_scratch/combined-update-health-full-importer-clean-99a9e54d.log`,
  SHA-256 `91c5f841ddff66e99b2792e39ae68ba4841fe7f1c90780ed0503727254286d6b`.
- Affected Q31/Q34/Q47/Q48 source suites passed 6/6, 11/11, 18/18 and
  11/11. External log SHA-256 values respectively:
  `8395913635d4fc9f813367c3b6071287752cdaa5d5a64766bfe362db1b78dfa1`,
  `dca5dc3b0e72ad7a3c47e20acaf6993643ef4e22969a13f1ea1aef2744e7954a`,
  `1975cdc832961d896bddac59bbd71a50c82e300d8a8f877063e41708f6dc5ff6`,
  `6e425ec735baabdc75d9d4fc9f8363943d3a881d286bd8315d99bfab87afd83e`.
  Q34's five preview changes were restored before the clean full-suite run.

## Deterministic local artifacts

From the clean `99a9e54d` source, `export-pack`, `changelog preview`,
`release bundle`, `release validate`, `release draft` and
`release draft-validate` all exited 0. Their external log SHA-256 values in
that order are:

1. `83151ebceb58573bc4f203f7f074c592a537726ef5c308e024f06e6363cb5a0d`
2. `e7033a49f8f740c3ee96c666cf1cd385e2e253ddb79803476bbf992efda1ea54`
3. `3ce86b6ae4eb166e2e7d76d68a57e0f77896082461572a17fe17e43884b40090`
4. `8e0f105a0248c91c957c90ebcd1acf09012fa479f088fc3fb3f0fe78f6352a07`
5. `88da611652e9735e3077ac53c17af3496a8231375bf530f7922e9ea9537b66bb`
6. `13103d0bfd1ae6bd60f6e12e9c4d0a9337f3e68b7f599f35c72d82634b8545de`

The local ZIP SHA-256 is
`32c1f0ad5465809eec5d8ed64c801e8d3ca31c0fe5840ca41188a376325711f9`;
tar.gz SHA-256 is
`22101aa98982cf8b88d6a4540d814e9751095207535427a4e5a5fc3f36833044`.
`release-provenance.json` binds both to source `99a9e54d` with
`dirty_state: false`, `preview_only: true` and `no_publish: true`.
Canonical `validate`, `doctor` and `pack-status` each exited 0 after
generation; log SHA-256 values respectively:
`8f29206e28139058f06530d39e09125c3e12d8a962b4034cb1309e15bf34a8a4`,
`0c1351ded532d4b7d924d989190cf25fbe57be2ac41c63da5546689087ddacf8`,
`6dfead5e9ffb41f8a52d930554e3db5ba710ec78dc87266a9b3d7e5b304bc41d`.
Pack provenance and boundary passed with zero problems.

## Extracted consumer and independent artifact verdict

- The reviewed external canary script SHA-256 is
  `70c2e9dce144bf3bd3212dd5df3b20fb56726d5fe8249f7f135bfe38595fc0e4`;
  its prior independent scoped ACCEPT report SHA-256 is
  `ef83c612e6d0bd1a4f1c889845b18e859e018ce55f819b6595a12b81993c03b7`.
- Exact run `D:/Projects/AIDE/_review_scratch/three-way-update-consumer-prep/run-99a9e54d-20260925-2024`
  exited 0, 25 delivered CLI commands, including five expected exit-2
  refusals. Summary SHA-256:
  `01b7f9515b9e8da3f125043dc3501c34bcf3ddf2fc409a9474bfdf5452ec901e`;
  run-log SHA-256:
  `9985c515fcea16a7308593d7160841f5ae97cd8b86e0a9eef94f3e5397c067c6`.
  ZIP/tar member maps matched at 833 files. The canary exercised installed
  fresh import, two synthetic successive updates, disabled optional content,
  missing-owned-file refusal and repair eligibility, direct-edit explanation,
  authored CRLF `AGENTS.md`, two project-selected conflict resolutions,
  read-only health states and no feedback by default.
- Independent exact artifact/consumer `ACCEPT_WITH_NOTES`:
  `D:/Projects/AIDE/_review_scratch/update-repair-health-99a9e54d-artifact-review.md`,
  SHA-256 `8bfcde284e827893b8a2772f4c52c1de3ca95c58e93f1d7a13fefbb913307bfb`.
  It independently checked archive safety, 830 embedded checksums, nine asset
  hashes/sizes, seven release-core checksums, source CLI bytes and all 25
  command logs. Its notes are nonblocking for this bounded **local preview and
  source-integration** decision: the V2/V3 packs are synthetic, CLI binding
  does not prove the whole source tree, no OS-level traffic trace was run, and
  this canary does not qualify repair apply, rollback, removal apply, hostile
  concurrency, native/hosted effects or public download. Those requirements
  remain with the parent campaign and final release profile.

## Open effect gate

Commit these exact generated outputs, prove post-commit deterministic replay
and range/canonical checks, then obtain an independent exact `dev` effect
verdict. Refresh local/remote refs and authentication before the one-writer
fast-forward and normal push. No main promotion, tag or publication is
authorized by this evidence alone.
