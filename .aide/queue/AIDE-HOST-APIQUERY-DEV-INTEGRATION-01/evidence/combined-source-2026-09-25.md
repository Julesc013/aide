# Combined isolated-host API-query source checkpoint

Base dev `fce11e7fce3e8106a71f5a2391fd6f0517d7e0c8` was clean. The
published source candidate `ad1076a3b165d15bfb68045908dfef1f5acd13c2`
has tree `db819d476dc4a483f5e0a033fba9787097c0f949` and is an
evidence-only descendant of independently reviewed repair
`1011d008fc39b135a5ef27062b5b8ee9c95cdc7f` (tree
`68cbc4d2b15049b7c589204d29003cf4affd93fc`). That review passed source
with 140 permitted tests; it did not qualify a native effect.

The actual no-commit merge found four documentation conflicts:
`DOCUMENTATION.md`, `IMPLEMENT.md`, `PLANS.md`, and
`docs/reference/integration-broker-core.md`. Both sides' substantive content
was retained. Runtime source, direct tests, queue index, and task evidence
merged without textual conflicts. The source candidate added no generated
portable or release artifacts to this merge. No native API object or real host
query was created by the integration run.

| Check | Observed result |
| --- | --- |
| Permitted combined-source tests | 140/140 PASS in 1.518 seconds |
| Excluded effect tests | Three `NativeApiSetQueryApi` synthetic-object tests and one live loopback test, explicitly not run |
| Exact C default commit range | PASS_WITH_DISPOSITIONS; `1011d008-api-query-why-bullet` accepted |
| Exact C raw range | FAIL on the original missing `## Why` bullet |
| Canonical validate and doctor before merge commit | Exit 0 on staged source |
| Canonical validate and doctor immediately after `ab17fd66` | Exit 1; the older pack manifest still named source `3326868b` |
| Staged diff whitespace | PASS |

The test runner and logs are external at
`D:\Projects\AIDE\_review_scratch\host-dev-permitted-tests.py` and
`host-dev-permitted-tests.log`; range, validate, and doctor logs are in the
same directory with `host-dev-` prefixes. These tests do not establish physical
host bytes, restricted principal, native query, private image/grants,
AppContainer Python, hosted target, credential/model, or activation guarantees.

The two-parent source merge was committed at
`ab17fd664159c46fa40e4683f8a4276c452a34a1` (tree
`b0baf9f4f3fdb33399383a7986c21ec697ae9723`). An independent Codex
GPT-6 Sol reviewer, `/root/host_candidate_review`, returned
`ACCEPT_WITH_NOTES` **for this source merge only**. The reviewer verified exact
source-manifest hashes, both parents, documentation reconciliation, the sound
140/4 test selection, and the accepted C disposition with raw failure.
After reading the actual post-commit logs, the reviewer explicitly held final
artifact/canonical qualification and dev fast-forward: `validate` and `doctor`
failed because the existing portable manifest still named source `3326868b`.
The original precommit exits must not be cited as final canonical passes.

The current generator was then run with `export-pack` **first from clean
`ab17fd66`**, followed by `changelog preview`, `release bundle`, and
`release draft`. The new pack manifest records source `ab17fd66` and
`source_dirty_state: false`. Pack status, local release validation, draft
validation, canonical validate, and doctor now exit zero. The current ZIP
SHA-256 is `515817522aba08281cb7f61a55185fbdc315b861d002d2008b3a3d94d7235411`
and tar.gz is
`c5def15fc3920d25aad095ede0ea4f39966f8cff2e082c4ba06facb5414d5bbb`;
the final post-commit replay remains pending. This remains a local preview
with no tag, upload, or publication.

## Refreshed local projection and affected suites

| Check | Observed result |
| --- | --- |
| Export/import suite | 29/29 PASS in 388.557 seconds |
| Local release bundle suite | 18/18 PASS in 45.330 seconds |
| Local GitHub release draft suite | 11/11 PASS in 22.711 seconds |
| Portable governance suite | 6/6 PASS in 52.382 seconds |
| Changelog preview | PASS; zero malformed in latest 50 commits |
| Current pack status | PASS provenance, checksums, and boundary |
| Release validate and draft-validate | PASS, preview-only, no publication |
| Canonical validate and doctor after regeneration | Exit 0 |
| Repeated preview, bundle, validate, draft, draft-validate | 33 changed generated paths compared, zero byte changes |

The stable replay hash map is external at
`D:\Projects\AIDE\_review_scratch\host-dev-replay-before.json`; logs share the
`host-dev-replay-` prefix. The export/import and Q47/Q48/Q31 suite logs use
`host-dev-` prefixes in the same directory. These results qualify a local
artifact projection from source `ab17fd66`; the projection still requires a
commit, then post-commit provenance and replay checks. The independent source
review explicitly retains its artifact hold until that exact later candidate
is checked.

The refreshed projection was committed at
`3875cad7af78aeefdc26d2557a1a254edf49b98f` (tree
`2d7bda9e9ce3b30ce93bc4da623e75d2316e1781`). Post-commit pack status
became `PASS_SOURCE_ANCESTOR`, with checksum and boundary checks still passing.
Release and draft validation passed. Replaying bundle, validation, and draft
from the committed source-ancestor state changed 15 of 44 local release files,
mainly metadata recording the corrected status; validation reports also
updated. A subsequent full replay changed zero of 44 files. The ZIP and tar.gz
digests above did not change. This stable source-ancestor metadata requires its
own commit, followed by final post-commit replay and narrow artifact review.
