# Owned-file repair implementation evidence

## Changed files

- `.aide/scripts/aide_lite.py`: `repair-owned-file` CLI, exact pack/receipt/ownership/missing-preimage gates, plan identity, exclusive repair intent/recovery, shared lifecycle lock with installed-pack import, Windows pinned directory handles and handle-relative no-clobber publication.
- `.aide/scripts/tests/test_export_import.py`: repair regressions covering extracted-pack CLI, stale plan, local edit, tampered pack/receipt, wrong validated pack, unsafe path, interruption, unknown post-interruption bytes, competing creation at publication, prepublication retry, overlapping repair/import, and parent substitution.
- `docs/reference/cross-repo-pack-export-import.md`: bounded consumer procedure and limitations.
- `.aide/queue/AIDE-DELIVERED-PACK-OWNED-REPAIR-APPLY-01/**`, `.aide/queue/index.yaml`, `PLANS.md`, `IMPLEMENT.md`: queue admission, plan, state, and execution record.

## Validation commands and results

- `py -3 -m unittest discover -s .aide/scripts/tests -p test_export_import.py` — PASS, 32 tests. This run began before the final fourth repair case was added.
- Initial focused `unittest.TestSuite` of four `test_owned_repair_*` methods in `test_export_import.py` — PASS, 4 tests, including an extracted-pack CLI invocation.
- Final focused `unittest.TestSuite` of six `test_owned_repair_*` methods — PASS, 6 tests in 98.731s.
- Independent exact `49f38d12` review — `REQUEST_CHANGES`; reviewer reported full importer suite 35/35 PASS and diff check PASS, while identifying source-derived concurrent-intent and parent-substitution races. This verdict is not acceptance evidence.
- Focused overlapping repair/import and parent-substitution tests — PASS, 2 tests in 38.618s.
- First post-review full importer suite — FAIL, 36/37 passed in 661.636s. The sole failure was a test-injection error: its mock interrupted the new intent publication instead of the intended payload publication. The hook was narrowed to the payload leaf; the corrected single test PASS in 24.370s.
- Corrected final full importer suite: `py -3 -m unittest discover -s .aide/scripts/tests -p test_export_import.py` — PASS, 37 tests in 744.824s.
- Owner inspection before superseding commit found a fresh-install lock gap: imports with no receipt bypassed the lifecycle guard. This could overlap a second first import and then a repair. The wrapper now guards all effectful imports, and the guard writes no lock file to the target on Windows. A new deterministic first-install test invokes nested import and repair plus an extracted-CLI import in another Windows process at the first payload boundary.
- Focused fresh-install overlap, installed repair/import overlap, and parent-substitution tests — PASS, 3 tests in 59.983s.
- Final 38-test importer suite after private POSIX lock-file hardening — PASS, 38 tests in 670.154s, exit 0. Exact runner summary: `evidence/full-importer-suite-summary.txt`.
- The final runner summary is SHA-256
  `c7844241c6b2f6bf6605de52d8a6676a8c8e7888d1a19de1dd5bac3d7a37d881`.
  Final code SHA-256 is
  `28387e55b05b07d2b4a649ecba989f759abeb7bce9c30298649356252d8ba5d0`;
  final test SHA-256 is
  `7a64771ffddd02170fe10fb7e1d92f23c3e9e41bacb1f85efd36457f507f4a9f`.
- Canonical `py -3 .aide/scripts/aide_lite.py doctor` — FAIL because validation has failures.
- Canonical `py -3 .aide/scripts/aide_lite.py validate` — FAIL on two pack-provenance checks: committed export manifest source commit `3326868b534d6a514af14c4ca3aabc9dc8230579` differs from task HEAD `49f38d12f425b32c19b4bda74bb288007c90952a`. No generator/export/release outputs were changed in this implementation worktree.
- `py -3 -m py_compile .aide/scripts/aide_lite.py .aide/scripts/tests/test_export_import.py` — PASS.
- Earlier base-source `doctor` and `validate` runs passed before the later
  source candidate advanced beyond its generated export pack. They do not
  supersede the current canonical provenance failures above.
- `git diff --check` — PASS.

## Result and retained boundaries

The positive consumer path restored the exact missing bytes and cleared its intent. Dry-run and stale-plan refusal produced no repair write. An existing project edit, wrong exact pack, tampered receipt, and unknown bytes after interruption remained untouched. A competing file created at the final publication boundary is preserved by atomic no-clobber creation, with its intent retained for review. All effectful imports and repair share an exclusive per-target guard; Windows creates no target lock file, while POSIX import retains a private temporary lock file to preserve lock inode identity. Windows path components are pinned against rename and reparse traversal for repair-intent and repair-payload publication. The existing importer payload writer still uses its prior full-path atomic replace and does not gain the repair path's parent-substitution guarantee in this slice. Only one missing managed file from the exact recorded safe-mode pack is supported. Non-Windows repair apply fails closed. Managed-section repair, altered-file reconciliation, rollback, removal, live-target adoption, archive publication/provenance signing, and regenerated shared pack/release outputs remain deferred. Abrupt termination before staged-file cleanup can leave an unreferenced hidden temporary file; no automatic cleanup is claimed. No commit, branch/ref operation, or target repository outside disposable tests was performed. Independent review is pending.
