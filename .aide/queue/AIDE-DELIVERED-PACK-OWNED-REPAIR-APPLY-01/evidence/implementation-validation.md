# Owned-file repair implementation evidence

## Changed files

- `.aide/scripts/aide_lite.py`: portable `repair-owned-file` CLI, exact pack/receipt/ownership/missing-preimage gates, plan identity, repair intent/recovery, atomic no-clobber publication, importer interlock, target-path hardening.
- `.aide/scripts/tests/test_export_import.py`: six repair regressions covering extracted-pack CLI, stale plan, local edit, tampered pack/receipt, wrong validated pack, unsafe path, interruption, unknown post-interruption bytes, competing creation at publication, and prepublication failure retry.
- `docs/reference/cross-repo-pack-export-import.md`: bounded consumer procedure and limitations.
- `.aide/queue/AIDE-DELIVERED-PACK-OWNED-REPAIR-APPLY-01/**`, `.aide/queue/index.yaml`, `PLANS.md`, `IMPLEMENT.md`: queue admission, plan, state, and execution record.

## Validation commands and results

- `py -3 -m unittest discover -s .aide/scripts/tests -p test_export_import.py` — PASS, 32 tests. This run began before the final fourth repair case was added.
- Initial focused `unittest.TestSuite` of four `test_owned_repair_*` methods in `test_export_import.py` — PASS, 4 tests, including an extracted-pack CLI invocation.
- Final focused `unittest.TestSuite` of six `test_owned_repair_*` methods — PASS, 6 tests in 98.731s.
- `py -3 -m py_compile .aide/scripts/aide_lite.py .aide/scripts/tests/test_export_import.py` — PASS.
- `py -3 .aide/scripts/aide_lite.py doctor` — PASS.
- `py -3 .aide/scripts/aide_lite.py validate` — PASS.
- `git diff --check` — PASS.

## Result and retained boundaries

The positive consumer path restored the exact missing bytes and cleared its intent. Dry-run and stale-plan refusal produced no repair write. An existing project edit, wrong exact pack, tampered receipt, and unknown bytes after interruption remained untouched. A competing file created at the final publication boundary is preserved by atomic no-clobber creation, with its intent retained for review. Import refuses a pending repair intent. Only one missing managed file from the exact recorded safe-mode pack is supported. Managed-section repair, altered-file reconciliation, rollback, removal, live-target adoption, archive publication/provenance signing, and regenerated shared pack/release outputs remain deferred. Abrupt termination before staged-file cleanup can leave an unreferenced hidden temporary file; no automatic cleanup is claimed. No commit, branch/ref operation, or target repository outside disposable tests was performed. Independent review is pending.
