# AIDE Release Notes Preview

This is a deterministic preview only. It does not publish a release.

source_range: HEAD~1..HEAD
source_head: d5e3e818841931702cd4e2cde49452744afab985
preview_only: true

## Highlights

- Added: report-only capability reality ledger support and generated capability reports. (d5e3e8188419)
- Added: X-OS-02 unit and golden coverage. (d5e3e8188419)

## Validation Summary

- d5e3e8188419: PASS: py -3 .aide/scripts/aide_lite.py verify, validate, doctor, test, selftest, eval run, export-pack, pack-status, review-pack, and capability status/scan/ledger/overclaim-report/validate.
- d5e3e8188419: PASS: py -3 .aide/scripts/aide_lite.py verify, validate, doctor, test, selftest, eval run, export-pack, pack-status, review-pack, and capability status/scan/ledger/overclaim-report/validate.

## Known Risks

- d5e3e8188419: X-OS-02 remains review-gated at needs_review.
- d5e3e8188419: X-OS-02 remains review-gated at needs_review.

## Follow-up

- d5e3e8188419: Run human review through AIDE-CHECK-OS-01 before any apply-capable Task OS phase.
- d5e3e8188419: Run human review through AIDE-CHECK-OS-01 before any apply-capable Task OS phase.

## Warnings

- None.

## Preview Caveat

- This draft is not an official release note and does not create tags or GitHub Releases.
