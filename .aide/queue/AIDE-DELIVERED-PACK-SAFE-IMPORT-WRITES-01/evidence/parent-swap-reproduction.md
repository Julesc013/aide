# Windows importer parent-swap reproduction

- Exact baseline: task admission `f3e6685139756007cc004e8593c235dc0b6f5cb7`
  on remote-observed dev `5dfa75e632b09f732a8150376db6840bcf149ed3`.
- Test: `ExportImportTests.test_import_payload_does_not_follow_a_swapped_parent`
  in `.aide/scripts/tests/test_export_import.py`.
- Fixture: two siblings under a temporary directory, `target` and `outside`.
  A copied managed prompt was planned for `target/.aide/prompts`. Immediately
  before the importer's `tempfile.mkstemp`, the test renamed that empty parent
  inside the temporary target and created a Windows junction to `outside`.
- Actual current-source outcome: the test **failed** on the no-outside-write
  assertion; `outside/compact-task.md` appeared. This is a reproduced safety
  defect, not an accepted passing test. The fixture cleanup removed the
  junction and temporary directory; no real target repository was touched.
- Command: `py -3 -B .aide/scripts/tests/test_export_import.py
  ExportImportTests.test_import_payload_does_not_follow_a_swapped_parent -v`.
  Exit code `1`; one test, one intended failure. External log:
  `D:/Projects/AIDE/_review_scratch/safe-import-parent-baseline.log`, SHA-256
  `180f77ac6ec746b15531fd92b12f9bdc3a2d76be02e189861e4f9fe386fbf4f2`.
- Acceptance requires this test to pass with an exercised staging boundary,
  with no outside temporary or final file, and the full importer suite and
  extracted delivered consumers to pass afterward.
