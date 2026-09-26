# Publication input guard repair, 2026-09-26

Independent reviewer `/root/partial_recovery_review` returned REQUEST_CHANGES
for `052a0a9265274975e4fea62655dc4eee7783017a`, tree
`6ff923c8392136d5aaa2c557b1ba3cf31499ab91`: a controls insertion at intent
retirement still returned success with a stale receipt. External original:
`D:/Projects/AIDE/_review_scratch/stable-lite-forced-restart-20260926/partial-import-source-rereview-052a0a92.md`,
SHA-256 `509bbf827f1d22957f6190cbd35c7aa6eaf1f2644de5b324c0d02b8d073981f7`.
No artifact or integration approval was granted. The attempted earlier child
rereview was rejected by an automatic safety filter before execution; it was
not a technical verdict. A separate independent reviewer supplied this report.

The repair pins existing controls and manual resolution files through receipt
publication and intent deletion. For absent controls it creates an exclusive,
temporary CREATE_NEW/DELETE_ON_CLOSE reservation beneath pinned directories.
A competing existing file refuses acquisition; close or process termination
removes only the created reservation. No persistent customization is authored.

PASS: `test_explicit_partial_recovery_finishes_fresh_and_predecessor_update`
(1 test, 46.430 seconds). PASS: one three-test command covering
`test_missing_controls_guard_blocks_writer_and_cleans_after_process_exit`,
`test_partial_recovery_blocks_controls_change_during_publication_and_retirement`,
and `test_partial_recovery_requires_exact_manual_resolution_bytes`
(3 tests, 131.711 seconds). It included a separate Python writer denial and a
child `os._exit(77)` cleanup observation. These are source tests, not delivered
archive qualification. The previous full suite was stopped with exit 1 after
the source rejection; no passing suite result is claimed.

Next: exact independent source rereview, one final full importer run, canonical
checks, current-generator projection and delivered restart consumer. Dev/main,
tag, publication and downloaded-byte acceptance remain separate unfinished gates.
