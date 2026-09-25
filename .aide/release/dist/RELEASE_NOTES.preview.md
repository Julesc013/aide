# AIDE Release Notes Preview

This is a deterministic preview only. It does not publish a release.

source_range: HEAD latest 50 commits
source_head: 8365aa61b7cad51d542f88434e50bc33c5aac8fe
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
- Changed: Track the bounded stable release contract as a campaign WorkUnit. (74093ecacb4f)
- Changed: Define a reviewable candidate for the first stable Lite release contract. (aa3bcfec849e)
- Changed: Refresh local portable-pack and release-preview outputs for qualified combined source. (d137f936bf0a)
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

- 10a16afb681e: PASS: clean convergence commit 9f2f3895 replay changed zero of 44 release files.
- 6377cda923c1: PASS: dev and origin/dev fast-forwarded from 9a8b0870 to 10a16afb; Git and GitHub refs agree.
- 7624d9f4b542: PASS: Python compilation and staged diff whitespace check on the combined source.
- d13894ba0f55: PASS: ten adversarial Windows removal tests with the frozen shared-helper snapshot and three existing planner tests.
- 0fbabcdd8510: PASS: 55 combined importer tests and 46 affected Q31/Q34/Q47/Q48 tests.
- 515ad6b2c07e: PASS: all four post-commit generators returned zero.
- fbd9465344f0: PASS: Twelve focused removal tests passed in 185.261 seconds using frozen helper snapshot injection; four affected tests passed in 73.470 seconds.
- 5317524f0760: PASS: task inspect classifies the WorkUnit complete with zero missing evidence.
- 009668559436: PASS: source compilation and staged whitespace check.
- b05ba7d5984f: PASS: checkpoint identities checked against local worktrees and observed remote dev.

## Known Risks

- 10a16afb681e: This evidence-only change does not alter the reviewed source or artifacts; post-link cleanup remains an uncertain recovery effect.
- 6377cda923c1: Post-link cleanup uncertainty and safe import, removal, rollback, native/hosted, main, and release gates remain open.
- 7624d9f4b542: The importer update has a visible missing-leaf interval and manual backup reconciliation; stable release qualification is separate.
- d13894ba0f55: Authored brownfield AGENTS remains partial; anchored managed-section edit and general rollback remain open.
- 0fbabcdd8510: Current generated bytes are a local preview; release and native/hosted qualification remain separate.
- 515ad6b2c07e: Local preview metadata is not stable release publication.
- fbd9465344f0: The task branch still depends on shared lifecycle helpers from newer dev ancestry. Already absent paths now yield partial removal; authored brownfield AGENTS.md section removal is not implemented.
- 5317524f0760: Parent campaign still requires removal, rollback, native/hosted, main, and stable release qualification.
- 009668559436: Authored brownfield managed-section detach and general rollback remain unfinished; no dev effect is authorized by this source merge alone.
- b05ba7d5984f: Main promotion, tag, publication, native/hosted qualification, and mandatory lifecycle closure remain open.

## Follow-up

- 10a16afb681e: Refresh dev and origin/dev, fast-forward only if ancestry holds, push normally, and observe the remote ref.
- 6377cda923c1: Reconcile the safe-import candidate against current dev while retaining the exclusive repair helper and lifecycle lock.
- 7624d9f4b542: Finish exact combined tests and review, regenerate current-source pack/release bytes, then qualify before dev integration.
- d13894ba0f55: Merge with accepted shared-helper ancestry, run combined tests and independent review, then qualify delivered consumers before dev effect.
- 0fbabcdd8510: Obtain the artifact verdict, converge post-commit metadata, and qualify exact dev integration.
- 515ad6b2c07e: Prove zero-change replay, then integrate the qualified candidate into dev.
- fbd9465344f0: Obtain independent rereview of this exact commit, reconcile into current dev with the shared helpers, and run combined and delivered-artifact qualification before integration.
- 5317524f0760: Continue dependency-ready lifecycle implementation and final release gates under the active parent goal.
- 009668559436: Complete combined tests and review, regenerate and qualify current-source artifacts, then decide dev integration.
- b05ba7d5984f: Resume combined removal qualification, then proceed through remaining mandatory product and release gates.

## Warnings

- None.

## Preview Caveat

- This draft is not an official release note and does not create tags or GitHub Releases.
