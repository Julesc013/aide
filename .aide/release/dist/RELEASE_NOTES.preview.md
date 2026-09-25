# AIDE Release Notes Preview

This is a deterministic preview only. It does not publish a release.

source_range: HEAD latest 50 commits
source_head: 99a9e54da887a3a209cfd73df345c55735819368
preview_only: true

## Highlights

- Security: Rollback no longer accepts a checksum-valid payload through a reparse pack boundary. (33824b369b84)
- Added: conditional receipt-owned removal apply for exact generated material. (d13894ba0f55)
- Added: bounded predecessor-pack rollback apply for the declared Windows slice. (23422130fcfc)
- Added: receipt-owned managed-section removal inside authored AGENTS.md on Windows, preserving all outside bytes. (d5b44626d6f9)
- Added: Local delivered pack evidence for supported rollback, owned removal, and interruption recovery. (db7650536375)
- Added: Bounded plan for manual portable-pack conflict resolution and disabled-feature preservation. (63484c756197)
- Added: Manual three-way portable-pack resolution and explicit optional-example disable survival. (acbcb9c8bd62)
- Added: Inspect the health of a delivered Lite installation without modifying its target. (03c5e7f81c22)
- Changed: Local release provenance now records clean ancestor status for the lifecycle pack. (0c048b3baeb7)
- Changed: Recorded local lifecycle release replay evidence. (7e8816b60af7)
- Changed: Recorded completed lifecycle dev integration evidence and next mandatory product gap. (d4b67c96ff81)
- Changed: Track installed Lite repair diagnosis as a bounded campaign task. (0aa5a9d23b10)
- Changed: Keep predecessor-bound import and rollback regressions aligned with the validated receipt contract. (c68077548ee9)
- Changed: Combine delivered update and read-only repair-health implementation for qualification. (99a9e54da887)
- Fixed: receipt-owned removal recovery preserves later authored bytes and retains ownership evidence when a recorded path was already absent. (fbd9465344f0)
- Fixed: Generated install guidance now describes the supported bounded removal apply path. (597b5bcd6f54)
- Fixed: Generated removal guidance now describes planner output and recovery states accurately. (49318d50472b)
- Fixed: authored AGENTS backup recovery retains receipt and intent until exact original backup cleanup is reconciled. (2c4c9089a546)
- Fixed: Pending portable removal now blocks exact-predecessor rollback preview and apply. (1f920ebbf7bf)
- Fixed: Exact predecessor rollback now accepts an unchanged authored CRLF AGENTS.md managed section. (9a0843c3a763)
- Fixed: Missing receipt-owned files now conflict instead of being silently recreated. (acbcb9c8bd62)
- Fixed: Receipt-owned CRLF AGENTS sections update when their upstream managed block changes. (3239530132a6)
- Fixed: Automatic managed updates now require a validated predecessor baseline instead of a local receipt claim alone. (12758e07373f)
- Fixed: Reject receipt claims that disagree with the delivered pack during installed health inspection. (486aa2bd0f5f)
- Fixed: Recognize valid CRLF portable guidance blocks during read-only installed health inspection. (558638203fae)

## Validation Summary

- ef60c1388ee5: PASS: export included 828 files with 831 checksum entries; bundle, release validation, draft, and draft validation exited zero.
- 3ed628c19aed: PASS: exact allowlist indentation assertion and canonical validate.
- e4697aaa3271: PASS: bundle, release validation, draft, and draft validation all exited zero on first replay.
- 6b4007d06546: PASS: independent ACCEPT_WITH_NOTES for e4697aaa, 42 importer and 46 adjacent tests, 16 consumer checks, and zero of 44 release files changed on replay.
- 9a8b08700ef7: PASS: both remote ref readings matched 6b4007d0; canonical validate and staged diff whitespace checks passed.
- fdad1a06f3fe: PASS: canonical validate and staged diff whitespace check on the admission record.
- 1a44ec617508: PASS: baseline regression demonstrated both old-helper stage writes.
- e215698a993d: PASS: setup-failure regression, one test with two Windows fault-injection subcases.
- 0dfb2931d32f: PASS: focused parent substitution, competing leaf, guarded staging, ordinary update and recovery tests on Windows.
- d4311651b76d: PASS: exact e215 importer suite, 44 tests in 617.176 seconds; focused repair suite, 11 tests.

## Known Risks

- ef60c1388ee5: Local draft and assets are no-publish evidence; full lifecycle, importer safety, and stable release remain open.
- 3ed628c19aed: This correction does not broaden the source or artifact review verdict.
- e4697aaa3271: Consumer qualification and independent exact-candidate acceptance remain pending for dev integration.
- 6b4007d06546: Importer write safety, full removal/rollback, native/hosted qualification, main, and publication remain open.
- 9a8b08700ef7: Dev contains repair source with disputed staging-file write safety; main and public release remain untouched.
- fdad1a06f3fe: Current dev repair helper is unsafe under the reproduced second-writer race; main and public release remain untouched.
- 1a44ec617508: A cleanup error after link publication is an uncertain effect requiring recovery review; no main or release effect is authorized by this commit.
- e215698a993d: A post-link cleanup error is an uncertain effect; the intent must be reconciled before retry.
- 0dfb2931d32f: Existing-leaf update has a visible missing-leaf interval; a rival leaf leaves an exact backup and requires manual recovery.
- d4311651b76d: A post-link stage cleanup failure remains an uncertain recovery effect; this is not main or stable-release acceptance.

## Follow-up

- ef60c1388ee5: Verify exact committed bytes through replay and disposable consumers, obtain independent review, then advance dev if accepted.
- 3ed628c19aed: Complete exact consumer checks and independent review before dev integration.
- e4697aaa3271: Run the full four-command replay from this clean commit and record zero-change evidence, then finish exact review.
- 6b4007d06546: Recheck remote dev and shared writer state, fast-forward qualified history, push normally, and observe remote identity.
- 9a8b08700ef7: Reproduce against the exact dev helper, close the race, review the fix, then resume lifecycle qualification.
- fdad1a06f3fe: Implement exclusive staged publication, test both repair intent and payload, then qualify exact dev candidate.
- 1a44ec617508: Complete combined qualification and independent review, then integrate the exact accepted candidate into dev.
- e215698a993d: Complete the running combined tests and independent exact-source review before dev integration.
- 0dfb2931d32f: Obtain independent source review, combined-source artifact qualification and dev integration.
- d4311651b76d: Finish extracted consumers and postcommit replay, obtain artifact review, then fast-forward qualified dev.

## Warnings

- None.

## Preview Caveat

- This draft is not an official release note and does not create tags or GitHub Releases.
