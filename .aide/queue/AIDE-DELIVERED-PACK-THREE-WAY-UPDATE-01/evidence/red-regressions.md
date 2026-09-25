# Red regressions on admitted update task base

- Task branch admission commit: `63484c7561978aa77fef067e7984164f2ed52946`,
  from `dev@d4b67c96ff81eb10aeecd6763b538331844619c9`.
- External test-only patch SHA-256:
  `215cecb5881266689bf11b86b40603afae5b6e05e4cf0a9cd24943dcfe28b732`.
  `git apply --check`, `git apply`, Python AST parse and `git diff --check`
  passed. Only `.aide/scripts/tests/test_export_import.py` changed at this
  red checkpoint; source was unchanged.
- `py -3 -B .aide/scripts/tests/test_export_import.py
  ExportImportTests.test_manual_three_way_resolution_keeps_local_overlay_across_updates`
  exited 1 after one test in 30.868 seconds. It first established current
  conflict-first refusal for a direct edit versus changed upstream pack,
  without changing target or receipt. Then it raised
  `TypeError: apply_import_pack() got an unexpected keyword argument
  'resolutions'`. External log
  `D:/Projects/AIDE/_review_scratch/three-way-update-red-test_manual_three_way_resolution_keeps_local_overlay_across_updates.log`
  SHA-256 `db76dd934e0f9add07a1421271c084322cab10af3056acb3ddf07b605c318a0b`.
- `py -3 -B .aide/scripts/tests/test_export_import.py
  ExportImportTests.test_missing_receipt_owned_file_refuses_implicit_recreation`
  exited 1 after one test in 25.318 seconds. Preview reported `PLANNED`
  rather than expected `PLANNED_CONFLICT` for a missing previously managed
  prompt. External log
  `D:/Projects/AIDE/_review_scratch/three-way-update-red-test_missing_receipt_owned_file_refuses_implicit_recreation.log`
  SHA-256 `bfed741fbc1c36ba826b65d740cc848254e681f909bbca8e3dc8acfdb1735111`.

These are intentionally failing source-baseline tests, not validation passes.
Implementation and green tests remain pending. The root controller retains
the queue, Git and generated-output write roles; source work is confined to
the three allowlisted source/test/user-guide paths in this worktree.
