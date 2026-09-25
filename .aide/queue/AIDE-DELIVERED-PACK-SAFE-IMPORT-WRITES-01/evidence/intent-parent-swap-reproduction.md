# Import intent parent-swap reproduction

- Baseline: task branch `e7c320cb` on dev ancestry
  `5dfa75e632b09f732a8150376db6840bcf149ed3`.
- Test: `ExportImportTests.test_import_intent_does_not_follow_a_swapped_parent`.
- An extracted portable pack was applied to a disposable target. Immediately
  before staging the target-local import intent, the fixture renamed the empty
  `.aide/install` parent and substituted a Windows junction to a disposable
  outside sibling.
- Current-source outcome: **failed as expected**. The importer created
  `aide-lite-pack-v0.intent.json` in the outside sibling. The junction and
  temporary fixture were removed; no real target was touched.
- Command: `py -3 -B .aide/scripts/tests/test_export_import.py
  ExportImportTests.test_import_intent_does_not_follow_a_swapped_parent -v`.
  Exit code `1`; one intended failure. External log:
  `D:/Projects/AIDE/_review_scratch/safe-import-intent-parent-baseline.log`,
  SHA-256 `2548173a8545615bf1bc531766f353ea6feb08721bb5f79b42b75f03b19be240`.
- Acceptance requires every effectful importer write, including intent and
  receipt metadata, to remain under an anchored target. Repairing only the
  managed payload write does not close this reproduced path.
