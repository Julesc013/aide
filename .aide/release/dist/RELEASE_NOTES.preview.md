# AIDE Release Notes Preview

This is a deterministic preview only. It does not publish a release.

source_range: HEAD latest 50 commits
source_head: 49318d50472b17f648c2f29e998239b9c446cf14
preview_only: true

## Highlights

- Added: restore a missing receipt-owned file from the exact delivered pack. (49f38d12f425)
- Added: receipt-backed read-only removal planning in the delivered portable CLI. (1a25e33effc5)
- Added: conditional receipt-owned removal apply for exact generated material. (d13894ba0f55)
- Fixed: receipt-owned removal recovery preserves later authored bytes and retains ownership evidence when a recorded path was already absent. (fbd9465344f0)
- Fixed: Generated install guidance now describes the supported bounded removal apply path. (597b5bcd6f54)
- Fixed: Generated removal guidance now describes planner output and recovery states accurately. (49318d50472b)

## Validation Summary

- 5ac617b37b57: PASS: canonical validation and diff whitespace check on the evidence-only closeout.
- fce11e7fce3e: PASS: independent evidence closeout hold cleared before the push.
- 526e9e402c56: PASS: current dev and candidate identities were checked before admission.
- ab17fd664159: PASS: 140 permitted combined-source tests; four effect tests excluded.
- 3875cad7af78: PASS: 140 permitted host source tests; 29 import, 18 release, 11 draft, and 6 governance cases.
- a4ee0f32ec7e: PASS: postcommit pack status reports PASS_SOURCE_ANCESTOR with valid checksums and boundary.
- a55b804bb573: PASS: independent source and artifact checks on the exact frozen subjects.
- 1c75abf1d93b: PASS: independent source, artifact, and narrow evidence reviews preceded dev mutation.
- 49f38d12f425: PASS: 32 importer cases before the final race repair; six final focused repair cases after it.
- 7bc4c9b5087b: PASS: exact dev/candidate/merge-base identities and historical B decision checked.

## Known Risks

- 5ac617b37b57: This closeout is not itself a source review or public release acceptance.
- fce11e7fce3e: Mandatory lifecycle apply, native and hosted qualification, main, and publication remain open.
- 526e9e402c56: Native and hosted qualification remain open; this task does not activate either.
- ab17fd664159: Physical host, restricted principal, native query, private image, hosted, and release gates remain open.
- 3875cad7af78: Post-commit provenance and independent artifact review remain; native, hosted, main, and publication are open.
- a4ee0f32ec7e: Final postcommit replay and independent artifact review remain; no public release or native effect is approved.
- a55b804bb573: This closeout does not qualify native or hosted effects, main, or public release.
- 1c75abf1d93b: Native, hosted, lifecycle, main, and publication qualification remains open.
- 49f38d12f425: Managed sections, modified files, rollback, removal, and live-target qualification remain open.
- 7bc4c9b5087b: This admission does not implement deletion or accept the old archive bytes.

## Follow-up

- 5ac617b37b57: Narrow-check this commit, then fast-forward qualified dev and observe remote identities.
- fce11e7fce3e: Integrate eligible removal and host source; implement the next lifecycle behavior gap.
- 526e9e402c56: Merge both histories, reconcile documentation, test combined source, and seek independent integration review.
- ab17fd664159: Seek independent exact combined-source review, then fast-forward dev only if accepted.
- 3875cad7af78: Check committed source ancestry, replay local outputs, and seek exact artifact review before dev mutation.
- a4ee0f32ec7e: Check exact final bytes and narrow review before the dev fast-forward.
- a55b804bb573: Narrow-check this evidence-only commit and then fast-forward dev after fresh remote checks.
- 1c75abf1d93b: Integrate eligible removal source and qualify the lifecycle repair candidate.
- 49f38d12f425: Obtain independent exact technical review; regenerate delivered artifacts on combined dev if accepted.
- 7bc4c9b5087b: Merge source, preserve current generator, regenerate outputs, and obtain independent review.

## Warnings

- None.

## Preview Caveat

- This draft is not an official release note and does not create tags or GitHub Releases.
