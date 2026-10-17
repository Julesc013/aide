# AIDE Release Notes Preview

This is a deterministic preview only. It does not publish a release.

source_range: 9a22aa0913965c41685105d0781a70ecad16696c..cba99132e729511b497e65ceb4f1c73cc4d6a29a
source_head: cba99132e729511b497e65ceb4f1c73cc4d6a29a
preview_only: true

## Highlights

- Changed: Record selected-task context proof and prepare its portable consumer checks. (bf15170f5a0d)
- Changed: Prepare portable context checks using the already completed export. (cba99132e729)
- Fixed: Context packets follow the recorded task selection and explain uncertainty. (6a50010b7160)

## Validation Summary

- 6a50010b7160: PASS: syntax and all 17 original binding method ASTs unchanged.
- bf15170f5a0d: PASS: source 61, no failures/errors/skips; job fully retired and collection verified.
- cba99132e729: PASS: source 61; ownership 6; export, doctor, validate and pack status.

## Known Risks

- 6a50010b7160: Recorded selection is not an atomic snapshot, active worker or permission.
- bf15170f5a0d: No active-worker, atomic snapshot, new release or whole-workflow claim.
- cba99132e729: Source documentation is not an exported pack member; no wider delivery claim.

## Follow-up

- 6a50010b7160: Qualify source, delivered payload and preview; review integration separately.
- bf15170f5a0d: Run one reviewed export job, then preview and separately reviewed integration.
- cba99132e729: Run final reviewed continuation and review terminal integration separately.

## Warnings

- None.

## Preview Caveat

- This draft is not an official release note and does not create tags or GitHub Releases.
