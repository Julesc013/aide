# Rollback reparse review repair

Date: 2026-09-25. Source-only candidate; no generated archive or dev effect.

## Finding and repair

Independent review of commit `23422130fcfc3a6e76e7e3c1e1c6697949730ae3`,
tree `40959f55ae9d04b780577a43af2cbb8057343178`, returned
REQUEST_CHANGES. Report
`D:/Projects/AIDE/_review_scratch/rollback-23422130-independent-review.md`
has SHA-256 `193cde85a9c2981bec211b8453298f9b9d2fe61dbcff40de2d059428044b851c`.
An owned Windows fixture made `pack/files` a junction to external fixture
bytes. The pack's checksums validated and the new safe-target enumerator
accepted the outside payload. No arbitrary target overwrite was demonstrated,
but the declared rollback pack boundary failed.

The repaired source rejects a reparse pack root, payload root, and manifest or
checksums metadata leaf before checksum reads, and keeps the descendant check.
It rejects either raw pack argument before resolving paths. The focused test
uses checksum-valid payload-root and pack-root junction fixtures and cleans up
those owned junctions explicitly.

## Verification

- The new one-test regression failed on `23422130` with `ValueError not raised`
  at the payload-root check, exit 1. It passed after the source repair.
- `py -3 -B -m unittest discover -s .aide/scripts/tests -p
  test_export_import.py -k rollback`: PASS, six tests in 177.988s, exit 0.
  Log `D:/Projects/AIDE/_review_scratch/rollback-reparse-repair-focused.log`,
  SHA-256 `74121b3db6f4274a77672dfa671dd710952ea5756aa7574bf2d61aafc88783cd`.
- `py -3 -B -m py_compile` on source and tests: PASS. `git diff --check`: PASS.
- Canonical `validate`: FAIL only at two export-pack/pack-status provenance
  checks, because this isolated source branch still has tracked pack source
  `7624d9f4` while HEAD is the original source commit `23422130` at test time.
  No generated output was refreshed in this WorkUnit. Log SHA-256
  `ffca7f2cc862910eaaf474f93f724030e6b7915a55275d7e5de74be5691d7c39`.
- Source `.aide/scripts/aide_lite.py` SHA-256
  `effd949be4872579f42e4ff530bbce828e55035c179f8e60bf3dd7420b90102e`;
  test `.aide/scripts/tests/test_export_import.py` SHA-256
  `77ec142388d80faf24f5b393eaa0d406712bd7d6f2071915c61a781e773f00b7`.

## Remaining gates

Freeze the superseding source commit and obtain independent delta rereview.
After acceptance, combine it with current dev, including the pending-removal-
intent gate, regenerate artifacts with the accepted release generator, run
delivered consumers and exact replay, then request an independent dev effect
review. Equal safe payload paths and an exact predecessor pack remain limits.
