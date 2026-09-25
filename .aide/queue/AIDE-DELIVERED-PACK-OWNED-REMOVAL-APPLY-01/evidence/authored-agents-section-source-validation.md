# Authored AGENTS section removal source candidate

Date: 2026-09-25. Isolated worktree
`D:/Projects/AIDE/aide-removal-combined`, branch
`task/aide-removal-combined-01`, starting HEAD
`ea53e319bd066efcdd0dc5ded38acd4f2d38c990`. This is a source
candidate for independent review; no dev/main, remote, generator, release,
or real target was mutated here.

## Exact behavior

- Windows receipt-owned removal now identifies one exact managed section in
  authored `AGENTS.md` as a candidate. It reads raw bytes so CRLF receipt
  digests remain valid and constructs the postimage by deleting only the
  validated section byte interval. All bytes outside that interval survive.
- The existing pinned Windows replace primitive checks the whole file digest
  at effect time and refuses a competing writer, redirected parent, multiple
  hard links or changed leaf. A digest-bound copy of the exact preview in the
  removal intent prevents rechecksummed intent edits from changing the
  authorized preimage. The intent retains pre/post digests and a deterministic
  backup path for interrupted replacement classification.
- A verified, exclusive-read postimage handle stays open through receipt and
  intent retirement. Any preserved or already absent recorded path still
  retains the receipt and runner as `PARTIAL_REMOVAL`. The exact generated
  whole-file `AGENTS.md` path remains a separate supported deletion case.

## Verification

- Initial brownfield regression: **RED as expected**, `PRESERVATION_REQUIRED`
  for an intact CRLF managed section because the old planner translated
  newlines. One test in 24.169 s, exit 1. Log:
  `D:/Projects/AIDE/_review_scratch/removal-brownfield-red.log`, SHA-256
  `7334ec9adca6f02f74df2ea9809c6ba873515afe31f8d162aa2421efb5bf69ad`.
- `py -3 -B -m unittest discover -s .aide/scripts/tests -p
  test_export_import.py -k removal -k brownfield`: **PASS**, 22 tests in
  428.761 s, exit 0. This covers authored prefix/suffix byte preservation,
  changed/duplicate blocks, exact preview, rechecksummed intent, competing
  writer, root junction, interruption/resume, unknown postimage, guarded
  receipt retirement, repeat refusal and generated whole-file removal. Log:
  `D:/Projects/AIDE/_review_scratch/removal-section-frozen-suite.log`, SHA-256
  `cc3e8b8f1c6cef9f157b157bdf346b497a6dc970c5709edc59a88086815820f4`.
- `py -3 -B -m py_compile .aide/scripts/aide_lite.py
  .aide/scripts/tests/test_export_import.py`: **PASS**.
- `git diff --check`: **PASS**.
- `py -3 -B .aide/scripts/aide_lite.py validate`: **PASS**, exit 0. Log:
  `D:/Projects/AIDE/_review_scratch/removal-section-validate.log`, SHA-256
  `7b326b01165e7743abe7d770bad1646dab78f4a411352dfbd8faae83b383e789`.

Exact SHA-256 source `.aide/scripts/aide_lite.py`:
`377399d6efabf184a6012fe42000295c71fd3add23a62bb2911e024b7ea8f4ae`.
Test `.aide/scripts/tests/test_export_import.py`:
`af2fc9786101970302c0a0da977f456089e5541e2c04253b6f4648c2403dc00f`.
Reference documentation:
`96ce9affb002a9c23315d80e0da010833f9f8bdf2bdb22ea77a14ca913f36b6d`.
Execution log `IMPLEMENT.md`:
`1a6c5879428d1438820a56cb9c7c60357d0486a4c9d5d52fcdbd01ec58b69899`.
Plan index `PLANS.md`:
`d2a65c2368b455caceec2856a4d14a66b780adccaadb2082fbac6806e1ebf839`.

## Retained limits

A failed anchored replacement may leave its original file under the
intent-recorded backup name. It is classified as uncertain and keeps the
receipt and intent; this source does not automatically move that backup into
place. Non-Windows apply remains unavailable. Full final artifact and
consumer qualification, independent source review, integration with the
separate rollback stream and exact dev effect are pending. This is not a
stable release or a claim that all lifecycle behaviors are complete.
