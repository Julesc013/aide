# Importer racing-leaf reproduction

- Baseline: safe-import branch `26720ed1` on dev ancestry
  `5dfa75e632b09f732a8150376db6840bcf149ed3`.
- Test: `ExportImportTests.test_import_payload_does_not_clobber_a_racing_leaf`.
- For both a new managed file and an update of an existing managed file, the
  disposable fixture changes the target leaf after the importer's preimage
  check and at its staging boundary. The concurrent bytes represent a project
  edit, and the test requires those bytes to remain intact.
- Current-source outcome: **failed as expected** in both subtests. The
  importer replaced the concurrent bytes with pack payload bytes. No real
  target repository was touched; temporary fixtures were removed.
- Command: `py -3 -B .aide/scripts/tests/test_export_import.py
  ExportImportTests.test_import_payload_does_not_clobber_a_racing_leaf -v`.
  Exit code `1`; one test, two failing subtests. External log:
  `D:/Projects/AIDE/_review_scratch/safe-import-leaf-baseline.log`, SHA-256
  `713a8c8a0aa192a2143f00e312efe58e04f5fd1f78d6a0bb6b7d7d32c047ca54`.
- Acceptance requires preserving a racing leaf in both cases, without
  treating the initial preimage check as final ownership proof. The repaired
  importer must also keep exact preview, receipt, recovery, and delivered
  archive behavior.
- Python compilation and `git diff --check` passed. Canonical `validate`
  exited `1` solely on two release/export provenance checks: this task's
  current HEAD `26720ed1` differs from the old generated pack's recorded
  source commit `1a25e33e`. The old pack is intentionally retained until the
  combined repaired source is ready for regeneration; this is not reported as
  a passing qualification. Full log:
  `D:/Projects/AIDE/_review_scratch/safe-import-leaf-validate.log`.
