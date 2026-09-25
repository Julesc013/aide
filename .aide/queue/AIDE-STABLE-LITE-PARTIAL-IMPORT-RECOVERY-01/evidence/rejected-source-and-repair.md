# Rejected partial-import source and bounded repair, 2026-09-26

The independent `/root/customization_review` source report for commit
`547ea2b09235e65c37f5009360caf0de3c63ae30`, tree
`3f3885ea3cc1ad6e8873376f29133ee71c51f016`, returned `REQUEST_CHANGES`.
External original:
`D:/Projects/AIDE/_review_scratch/stable-lite-forced-restart-20260926/partial-import-source-review-547ea2b0.md`;
SHA-256 `4dc3ab09f4930973c800c3e8c3fbfa8cdf7e81e919809a6febdf949d2cfbb5f4`.
It reproduced (1) a rewritten target intent that overwrote an authored file
and falsely recorded AIDE ownership, and (2) a controls-file insertion during
receipt publication that returned success with a stale controls digest. No
integration or release approval followed from that review.

The superseding source derives exact pack operation coverage and per-kind
action/ownership legality from the validated pack, prior receipt and exact
predecessor. It rechecks project controls and resolution inputs after the
receipt write, retaining the intent when either changed. On Windows, the
reviewer's authored-overwrite scenario first failed against `547ea2b0`
(authored bytes were overwritten), then passed against the repair. A second
regression inserts valid controls at receipt publication and now returns
`RECOVERY_REQUIRED` with the intent retained. A third regression removes an
included payload operation from a re-digested intent and now refuses.

The prior full importer suite was interrupted after the rejection; its partial
output is not a passing result. The repaired source still requires the full
importer suite, canonical validation, independent exact rereview, projection,
delivered-byte consumer and dev integration. Main, tag and publication remain
unperformed.
