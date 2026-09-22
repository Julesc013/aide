# Independent Review: Distribution Fixture Portability

Decision: `REQUEST_CHANGES` (initial review; superseded below)

Current decision: `PASS`

## Reviewed Identity

- Branch: `task/aide-distribution-fixture-portability-integration-01`
- Reviewed commit: `36fa64e011b56d228bdc83ed57ff78262934d762`
- Reviewed tree: `791cfe7599f052f5781096b630d3f5355bea5820`
- Reviewed parent: `7aab31bc1bc747484d80c662d20e218bb93d1f5b`
- Two-parent source merge: `7aab31bc1bc747484d80c662d20e218bb93d1f5b`
- Merge tree: `ad3e2746b08f8380abf7d6ddc793a8692460ecee`
- Merge parents: `f737f9199931131adce3bca430295754211f2e9a` and `e73ac0b269df3a47214588ae2d025d1b97f2f2c7`
- Original source commit: `e73ac0b269df3a47214588ae2d025d1b97f2f2c7`
- Original source tree: `b67c23b92d2086d2ed3862432a68a66af6861ea7`

The five source-candidate blobs are byte-identical at the original source
commit, the two-parent merge, and the reviewed HEAD. Both required ancestry
checks pass. Source identity and history are preserved.

## Ordered Findings

### F1 - HIGH - Windows 8.3 aliases can mutate an existing file

Locations:

- `core/distribution/temp_workspace.py:125`
- `core/distribution/temp_workspace.py:133`
- `core/distribution/temp_workspace.py:137`
- `core/distribution/operation_executor.py:151`
- `core/distribution/operation_executor.py:170`

`safe_join` rejects case-folded and NFC-equivalent child names, but it does not
verify that an existing Windows path was reached through the exact directory
entry name requested. On this machine's actual temporary volume, Windows
created the short-name alias `LONGFI~1.TXT` for
`LongFixtureNameForAlias.txt`. `safe_join(root, "LONGFI~1.TXT")` accepted that
alias and resolved it to the existing long-name file. A subsequent
`update_managed_file` operation with the correct preimage digest returned
`APPLIED_TEMP` and changed the long-name file from `keep` to `changed`.

This violates the ExecPlan oracle that aliased inputs are refused before
payload mutation and overstates the documentation claim that existing
child-name aliases refuse. The case requires no concurrent writer, symlink,
reparse point, hardlink, or elevated privilege.

Required changes:

- Detect and refuse alternate Windows directory-entry names, including active
  8.3 short-name aliases, before preimage reads or writes.
- Add a native Windows regression that creates a long-name file, obtains its
  actual short name when one is available, and proves both `safe_join` and
  operation execution refuse the alias without changing the file.
- Keep an explicit skip only when the test volume does not generate a distinct
  short name; do not count that skip as Windows alias qualification.
- Re-run the focused, adjacent, canonical, and exact-candidate checks and bind
  the repair review to the resulting new commit and tree.

## Validation

- PASS: exact branch, commit, tree, parent, and two-parent merge identities.
- PASS: original source commit is an ancestor of the source merge; the source
  merge is an ancestor of reviewed HEAD.
- PASS: all five source-candidate blobs are identical across `e73ac0b2`,
  `7aab31bc`, and `36fa64e0`.
- PASS: source-to-merge blob diff is empty.
- PASS: `git diff --check` for the source and combined candidate.
- PASS: commit-message range check for `f737f919..36fa64e0` (three commits).
- PASS WITH SKIPS: focused portability suite ran 125 tests: 117 passed, eight
  skipped, zero failed.
- PASS WITH SKIPS: adjacent `test_aide_distribution*.py` suite ran 156 tests:
  148 passed, eight skipped, zero failed.
- PASS: hardlink refusal and mocked Windows reparse-attribute refusal.
- REPRODUCED FAILURE: actual Windows 8.3 alias was accepted and used to mutate
  its long-name target.
- EXPECTED FAIL: `pack-status` reports valid checksums and boundaries with one
  provenance problem: manifest source `b3e5c7aa` does not equal reviewed HEAD
  `36fa64e0`.
- EXPECTED FAIL: canonical validation has two failed checks, both projections
  of that same stale portable-pack provenance condition.

## Skip And Provenance Assessment

The recorded eight skips are truthful: seven require symlink creation that the
current Windows token rejects with `WinError 1314`, and one requires an
unavailable FIFO. None is reported as qualified. The hardlink test and mocked
reparse-attribute test pass, but the skipped tests still prevent native
symlink behavior from being claimed for this Windows profile.

The recorded portable-pack gap is also truthful. Checksums and export
boundaries pass; the tracked manifest remains bound to
`b3e5c7aa2a1732faee4a9021e64bdba65c6db1cb` instead of the reviewed HEAD.
The changed `core/distribution` modules are not direct export-pack members.

## Residual Risks

- Static Python path checks remain a trusted-root, disposable, single-writer
  fixture boundary, not hostile-writer confinement or atomic target apply.
- Actual symlink behavior remains unqualified under this Windows token; a
  mocked reparse attribute does not replace an actual native symlink test.
- FIFO behavior remains unqualified on Windows.
- Component and aggregate path-length portability are not explicitly modeled;
  current preflight fails closed on filesystem errors but does not classify
  those limits lexically.
- Portable artifact provenance still requires a commit-bound refresh after a
  repaired candidate is integrated.

No Git history, branch, remote, target repository, release surface, machine
configuration, credential, or external service was mutated during this review.

## Superseding Rereview

Decision: `PASS`

### Repaired Identity

- Branch: `task/aide-distribution-fixture-portability-integration-01`
- Repaired commit: `64979977922ae8a493646df5858d0bd7f4459cd0`
- Repaired tree: `c7474c29bbd84dfce6fc08c892544da045b6db3a`
- Exact parent: `36fa64e011b56d228bdc83ed57ff78262934d762`
- Preserved source merge: `7aab31bc1bc747484d80c662d20e218bb93d1f5b`
- Original source commit: `e73ac0b269df3a47214588ae2d025d1b97f2f2c7`

The repaired commit, tree, and parent match the requested identities. The
original source commit remains an ancestor of the two-parent source merge and
the repaired HEAD; the source merge remains an ancestor of the repaired HEAD.
All five original source blobs remain byte-identical between `e73ac0b2` and
`7aab31bc`. At repaired HEAD, the intake and operation-executor blobs remain
identical, while the test, workspace helper, and reference document have the
intentional F1 repair changes. No source history was rewritten or lost.

### Finding Disposition

#### F1 - CLOSED - Windows 8.3 alias mutation

The repaired `safe_join` enumerates each existing parent and requires an
existing resolved component to have an exact enumerated directory-entry name.
An actual active Windows 8.3 alias was exercised on the current temporary
volume:

- Leaf alias `LONGFI~1.TXT` was refused by `safe_join` with
  `path_collision_refused`.
- `execute_operation` returned `FAILED_VALIDATION` with
  `distribution_apply_engine.path_collision_refused` and left the long-name
  file unchanged.
- Exact `LongFixtureNameForAlias.txt` lookup succeeded, and the corresponding
  exact-name operation returned `APPLIED_TEMP`.
- Nested parent alias `LONGDI~1/NestedLongFixtureNameForAlias.txt` was refused
  by both surfaces with zero mutation.
- Nested leaf alias
  `LongDirectoryNameForAlias/NESTED~1.TXT` was refused by both surfaces with
  zero mutation.
- The exact nested long-name path continued to resolve successfully.

This closes the original high-severity finding. No new material findings were
identified.

### Rereview Validation

- PASS: exact repaired commit `64979977`, tree `c7474c29`, and parent
  `36fa64e0`.
- PASS: original source-to-merge and source-to-repaired ancestry checks.
- PASS: all five original source blobs are byte-identical at `e73ac0b2` and
  `7aab31bc`; later blob differences are limited to the intentional repair.
- PASS: repair and full combined `git diff --check`.
- PASS: latest commit-message check.
- PASS: commit-message range `f737f919..64979977`, four commits.
- PASS: native active Windows 8.3 leaf, nested-parent, nested-leaf, exact leaf,
  and exact nested compatibility probe.
- PASS WITH SKIPS: focused portability suite ran 126 tests: 118 passed, eight
  skipped, zero failed.
- PASS WITH SKIPS: adjacent `test_aide_distribution*.py` suite ran 157 tests:
  149 passed, eight skipped, zero failed.
- PASS: `py -3 -B .aide/scripts/aide_lite.py test`.
- EXPECTED FAIL: `pack-status` reports valid checksums and boundaries with one
  stale-provenance problem: manifest source `b3e5c7aa` does not equal repaired
  HEAD `64979977`.
- EXPECTED FAIL: canonical validation has two failed checks, both projections
  of that same stale portable-pack provenance condition.

The eight skips remain truthful and unchanged: seven require symlink creation
that this Windows token rejects with `WinError 1314`, and one requires a FIFO
that Windows does not expose. The active 8.3 regression ran and passed; it was
not skipped.

### Residual Risks After Pass

- The helpers remain a trusted-root, disposable, single-writer fixture
  boundary, not hostile-writer confinement or atomic target apply.
- Actual symlink behavior remains unqualified under this Windows token; a
  mocked reparse attribute is not equivalent native symlink evidence.
- FIFO behavior remains unqualified on Windows.
- Component and aggregate path-length portability remain unmodeled lexically,
  although filesystem errors fail preflight closed.
- The committed native regression covers the active leaf alias. Nested aliases
  and exact-name compatibility passed an independent disposable rereview probe
  but are not separate retained regression cases.
- Portable artifact provenance still requires a commit-bound refresh after
  integration.

No Git history, branch, remote, target repository, release surface, machine
configuration, credential, or external service was mutated during rereview.
