# Receipt baseline and mapping repair, 2026-09-25

The independent review of frozen source `03c5e7f81c225525bc1b7bc9532f4353d0e42b07`, tree `d8954f98b234eb9c717cbeda197f71d0681a153e`, returned REQUEST_CHANGES. Actual reviewer report: `D:/Projects/AIDE/_review_scratch/repair-health-03c5e7f8-independent-source-review.md`, SHA-256 `1e2a76b5dc8cc35bfe0528d859245d8b7fdd9d033e54dd6350fcc5ee44cec835`. The exact-source probes showed that a re-digested receipt could report a directly edited file as HEALTHY, or claim an authored target using a different real pack source. Both probes preserved target bytes; the diagnosis was false.

The superseding source checks every receipt row's canonical kind/source/target and mode against the validated current pack manifest, then checks the receipt source digest against pack bytes. A receipt-owned installed digest must also match the pack baseline, allowing the existing LF/CRLF managed-section representation. Disabled entries cannot claim ownership. An invalid row remains UNKNOWN, has no repair plan, and makes the report PRESERVATION_REQUIRED. An intentional local overlay retains project ownership and unknown rationale, and the top-level report requires preservation rather than claiming whole-install health. The target path is reported lexically without following a rejected root symlink.

The new durable regression tests both forged baseline and wrong source-to-target mapping with exact before/after target byte equality. No repair apply or real target effect was performed.

Validation on the superseding uncommitted source in `D:/Projects/AIDE/aide-repair-health`, Windows Python 3:

- `py -3 -u -B -m unittest discover -s .aide/scripts/tests -p test_export_import.py -k repair_health_rejects_redigested -v`: exit 0, 1 test, 24.928 seconds. External log `D:/Projects/AIDE/_review_scratch/repair-health-forged-receipt-fix-tests.log`, SHA-256 `0f8a87c4537f9afaa53335930358cdb2f36a60d17a001f1125251cf210c84293`.
- `py -3 -u -B -m unittest discover -s .aide/scripts/tests -p test_export_import.py -k repair_health -v`: exit 0, 4 tests, 139.874 seconds, including extracted ZIP consumer/no-write, invalid/pending state, v1/v2 overlays/disabled, and both forged receipt cases. External log `D:/Projects/AIDE/_review_scratch/repair-health-focused-superseding.log`, SHA-256 `d4fbc9c3eb8600b5caed8225b8c6fedc9e2ddd4a4ce32a7ec7145b1a42aea6d0`.
- `git diff --check`: exit 0.

Source/test SHA-256 before freeze: `.aide/scripts/aide_lite.py` `84b41bf630b1963e3eb42aef1e8e08d2a3caf17d2438e10a5e64cb61e3714ffe`; `.aide/scripts/tests/test_export_import.py` `6bacbd6cb3c7420554b4ef213e49dcff5c60c5432737dc209b4067de03195296`.

Independent rereview of the superseding exact commit, combined tests/artifacts, and `dev` integration remain pending. The earlier REQUEST_CHANGES is retained and does not become an acceptance.
