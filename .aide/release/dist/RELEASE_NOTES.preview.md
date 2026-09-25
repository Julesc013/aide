# AIDE Release Notes Preview

This is a deterministic preview only. It does not publish a release.

source_range: HEAD latest 50 commits
source_head: 9a0843c3a7633002f91a0ec3e707fe613650eb5f
preview_only: true

## Highlights

- Security: Rollback no longer accepts a checksum-valid payload through a reparse pack boundary. (33824b369b84)
- Added: conditional receipt-owned removal apply for exact generated material. (d13894ba0f55)
- Added: bounded predecessor-pack rollback apply for the declared Windows slice. (23422130fcfc)
- Added: receipt-owned managed-section removal inside authored AGENTS.md on Windows, preserving all outside bytes. (d5b44626d6f9)
- Fixed: receipt-owned removal recovery preserves later authored bytes and retains ownership evidence when a recorded path was already absent. (fbd9465344f0)
- Fixed: Generated install guidance now describes the supported bounded removal apply path. (597b5bcd6f54)
- Fixed: Generated removal guidance now describes planner output and recovery states accurately. (49318d50472b)
- Fixed: authored AGENTS backup recovery retains receipt and intent until exact original backup cleanup is reconciled. (2c4c9089a546)
- Fixed: Pending portable removal now blocks exact-predecessor rollback preview and apply. (1f920ebbf7bf)
- Fixed: Exact predecessor rollback now accepts an unchanged authored CRLF AGENTS.md managed section. (9a0843c3a763)

## Validation Summary

- 5dfa75e632b0: PASS: remote refs and GitHub ref API returned the same dev SHA; local dev tree and ancestry were checked.
- f3e668513975: PASS: current dev identity and clean separate worktree checked.
- 26720ed197d0: WARN: the new test fails as intended on current source; it created outside/compact-task.md in a disposable fixture.
- e7c320cb8ec9: WARN: one new test fails as intended in two subtests on current source; concurrent bytes were overwritten.
- b2d159aa6c48: PASS: canonical doctor and validate on the observed dev base.
- f34947f6a78b: WARN: the new test fails as intended; an intent JSON appeared in the disposable outside sibling.
- 52b338eef8ff: PASS: final importer suite, 38 tests in 670.154 seconds; focused overlap and parent-race tests, Python compilation, and diff whitespace check.
- 01466f9e1814: PASS: diff whitespace check and source-location inspection.
- cd636c9ccd0d: PASS: six new adversarial tests against a frozen in-memory shared-helper snapshot; three existing planner tests; installed-runner check; compilation, doctor, validate, and diff whitespace check.
- ed366600dbc1: PASS: diff whitespace check and exact source/test hash comparison with precommit evidence.

## Known Risks

- 5dfa75e632b0: Removal deletion, real target rollout, main promotion, and publication remain unfinished.
- f3e668513975: Admission does not close the write race or qualify any target effect.
- 26720ed197d0: This commit contains the regression only; the stable importer remains unsafe under this race.
- e7c320cb8ec9: The importer source remains unsafe under these races until a reviewed repair is integrated.
- b2d159aa6c48: Current source remains read-only; a future apply must satisfy the retained technical gates.
- f34947f6a78b: Current importer metadata and payload writes remain unsafe under parent substitution.
- 52b338eef8ff: Importer payload writes remain pathname based and are being repaired separately.
- 01466f9e1814: This analysis does not make the current importer safe or qualify any delivered bytes.
- cd636c9ccd0d: This source must not be integrated or called complete before the reviewed helper, managed-section and receipt lifecycle, combined consumers, and independent review.
- ed366600dbc1: The branch is not qualified for dev integration or complete removal.

## Follow-up

- 5dfa75e632b0: Implement and qualify effect-time-owned removal and the remaining lifecycle journeys.
- f3e668513975: Add a deterministic failing junction regression, repair with reviewed handle primitives, and qualify delivered bytes.
- 26720ed197d0: Adapt importer publication using independently reviewed pinned-parent primitives, then rerun this and the full delivered suite.
- e7c320cb8ec9: Repair parent and leaf write boundaries, run full importer and archive consumers, obtain independent review, and regenerate combined artifacts.
- b2d159aa6c48: Implement adversarial tests and bounded effect code, then obtain independent review and combined artifact qualification.
- f34947f6a78b: Anchor all importer writes using reviewed primitives, protect racing leaves, qualify consumers, and obtain independent review.
- 52b338eef8ff: Obtain independent exact-candidate rereview, integrate accepted source with current dev, regenerate artifacts, and qualify combined consumers.
- 01466f9e1814: Integrate reviewed helper, implement source and recovery, pass adversarial and consumer tests, and obtain independent review.
- cd636c9ccd0d: Merge accepted shared lifecycle primitives, complete detach behavior, rerun actual combined tests and delivered consumers, then review and integrate.
- ed366600dbc1: Accept and merge the shared helper, complete detach, run combined tests and archive consumers, and obtain independent review.

## Warnings

- None.

## Preview Caveat

- This draft is not an official release note and does not create tags or GitHub Releases.
