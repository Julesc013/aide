# Windows repair staging source candidate

Base dev is `9a8b08700ef7356ee75b6750f3a53c97a4a56e3e`.
This source change gives each repair stage an exclusive Windows handle from
creation through handle-relative no-replace publication, then deletes the
stage link through that same handle. It applies to repair intent and owned
payload publication. The parent directory remains pinned during the effect.

The baseline adversarial regression failed in both stage subcases on the old
helper because the second process could write. External log:
`D:\Projects\AIDE\_review_scratch\repair-staging-baseline-regression.log`,
SHA-256 `9f68687d728b7dc59308810a00c1b0b39a5a9a1f761c1cdaab9f1f8b805f3cbd`.

On the changed source, `py -3 -B -m unittest discover -s
.aide/scripts/tests -p test_export_import.py -k test_owned_repair_`
passed 10/10 in 166.193 seconds, including both competing-stage-writer
subcases, no-clobber, interruption recovery, and the parent-substitution
attempt rehooked at publication. External log:
`D:\Projects\AIDE\_review_scratch\repair-staging-focused-repair-suite-v2.log`,
SHA-256 `6c36c9184c33fc1afe2d2dd7088f8449e98e1189219ceb106c0669c154db61ef`.

`py -3 -B -m py_compile .aide/scripts/aide_lite.py
.aide/scripts/tests/test_export_import.py` and `git diff --check` both passed.
The full importer suite, release-adjacent suites, generated-artifact replay,
consumer tests, and independent exact-candidate review are pending. No main,
tag, hosted, or public release effect follows from this source checkpoint.
