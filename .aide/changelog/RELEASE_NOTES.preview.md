# AIDE Release Notes Preview

This is a deterministic preview only. It does not publish a release.

source_range: 3dad27442fcf13e70cd02e633c6a38380b1e4959..f2184db7d4fc539c27887e2cea2bd3c73d409d36
source_head: f2184db7d4fc539c27887e2cea2bd3c73d409d36
preview_only: true

## Highlights

- Added: outcome lessons --path with human and JSON views. (99f91f6ceee9)
- Added: Portable source-linked lesson lookup with explicit invalidation. (f2184db7d4fc)
- Changed: Prepared portable qualification for current lesson retrieval. (9e60931b88f4)

## Validation Summary

- 99f91f6ceee9: PASS syntax and diff checks; NOT RUN source36 and actual lesson job.
- 9e60931b88f4: PASS source36, actual lesson, preserved ledger prefix and job retirement.
- f2184db7d4fc: PASS source36, delivered36, ownership6, doctor, full validation and pack status.

## Known Risks

- 99f91f6ceee9: Declared active lessons do not establish correctness or authorship.
- 9e60931b88f4: Matching evidence establishes bytes, not semantic correctness or permission.
- f2184db7d4fc: Advisory selection does not establish semantic truth or improved model results.

## Follow-up

- 99f91f6ceee9: Qualify source, delivered and installed behavior before integration.
- 9e60931b88f4: Run the reviewed consumer job, then qualify preview and integration.
- f2184db7d4fc: Run fixed preview, exact terminal review and qualified dev/main sync.

## Warnings

- None.

## Preview Caveat

- This draft is not an official release note and does not create tags or GitHub Releases.
