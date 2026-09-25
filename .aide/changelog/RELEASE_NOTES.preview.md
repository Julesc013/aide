# AIDE Release Notes Preview

This is a deterministic preview only. It does not publish a release.

source_range: HEAD latest 50 commits
source_head: 0509e1611b1838c650954c64212ad603f132dada
preview_only: true

## Highlights

- Security: Rollback no longer accepts a checksum-valid payload through a reparse pack boundary. (33824b369b84)
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
- Fixed: authored AGENTS backup recovery retains receipt and intent until exact original backup cleanup is reconciled. (2c4c9089a546)
- Fixed: Pending portable removal now blocks exact-predecessor rollback preview and apply. (1f920ebbf7bf)
- Fixed: Exact predecessor rollback now accepts an unchanged authored CRLF AGENTS.md managed section. (9a0843c3a763)
- Fixed: Missing receipt-owned files now conflict instead of being silently recreated. (acbcb9c8bd62)
- Fixed: Receipt-owned CRLF AGENTS sections update when their upstream managed block changes. (3239530132a6)
- Fixed: Automatic managed updates now require a validated predecessor baseline instead of a local receipt claim alone. (12758e07373f)
- Fixed: Reject receipt claims that disagree with the delivered pack during installed health inspection. (486aa2bd0f5f)
- Fixed: Recognize valid CRLF portable guidance blocks during read-only installed health inspection. (558638203fae)
- Fixed: installed Lite Task OS reports no selected task for an empty queue. (f00d937e2368)
- Fixed: project-owned Lite target queues no longer receive AIDE source-phase next-work advice. (e88a1468acd2)
- Fixed: target Task OS routing follows its declared profile even when a queue ID matches an AIDE source task. (b9d2b150c39c)
- Fixed: target next-work explanation remains accurate even when queue IDs collide with source IDs. (52e1f194ebd2)
- Fixed: local draft lifecycle claims now match the bounded Windows apply candidates. (bc1867a06933)

## Validation Summary

- 33824b369b84: New regression before repair: FAIL as expected (ValueError not raised).
- d5b44626d6f9: PASS: Twenty-two focused removal tests in 428.761 seconds, including interruption, competing writer, junction and repeat behavior.
- f2be45ea13ce: Primary and contributing worktrees clean before admission; remote dev observed at ea53e319.
- 2c4c9089a546: PASS: Eight affected authored-section tests in 247.733 seconds.
- 03f4b0a1ef37: Exact rollback source 33824b36 had independent source ACCEPT; current remote dev observed ea53e319.
- 1f920ebbf7bf: Red regression FAIL as intended, 1 test in 33.852 s, exit 1; green regression PASS, 1 test in 45.495 s, exit 0.
- 723322cf07ab: Exact removal source review ACCEPT_WITH_NOTES at 2c4c9089; eight affected author tests and independent backup fault injection passed.
- 9a0843c3a763: PASS: Red regression reproduced the AGENTS.md baseline error on source 723322cf; green regression passed after repair.
- db7650536375: PASS: Complete importer suite passed 85/85; affected Q31/Q34/Q47/Q48 suites passed 6/11/18/11.
- 0c048b3baeb7: PASS: First postcommit bundle, validate, draft, and draft-validate commands exited zero.

## Known Risks

- 33824b369b84: Hostile concurrent pack mutation and broader rollback path-set changes remain outside this bounded source candidate.
- d5b44626d6f9: An uncertain failed replacement can leave a recorded backup for manual recovery; non-Windows apply and final artifact qualification remain open.
- f2be45ea13ce: Authored-section removal source remains under independent review; this admission does not accept it.
- 2c4c9089a546: Independent source rereview and combined artifact qualification remain pending. Legacy intents without original identity fail closed if a backup remains.
- 03f4b0a1ef37: Pending-removal rollback interaction still needs a source guard and regression before integration acceptance.
- 1f920ebbf7bf: Authored-section source and delivered artifacts still require combination and qualification before a dev effect.
- 723322cf07ab: Source acceptance does not clear stale generated-pack provenance or qualify delivered bytes.
- 9a0843c3a763: The local archives generated from source 723322cf remain rejected and are not advanced to dev.
- db7650536375: These are local no-publish artifacts and do not qualify a stable release or hosted/native operation.
- 0c048b3baeb7: These files are local preview artifacts, not a public release.

## Follow-up

- 33824b369b84: Obtain independent exact delta rereview; combine with current dev and its removal-intent gate before artifact and consumer qualification.
- d5b44626d6f9: Obtain independent technical source review, combine with accepted rollback work, regenerate qualified artifacts and verify disposable consumers before a dev effect.
- f2be45ea13ce: Integrate accepted rollback source, repair any removal review findings, then qualify the combined delivered bytes.
- 2c4c9089a546: Review this exact source candidate, then regenerate and qualify combined artifacts before dev integration.
- 03f4b0a1ef37: Add the semantic guard, obtain combined review, then merge only independently accepted authored-section source.
- 1f920ebbf7bf: Merge independently accepted removal source and run combined lifecycle checks with the current release generator.
- 723322cf07ab: Run combined tests and independent review, regenerate current artifacts, qualify extracted consumers and replay before any dev effect.
- 9a0843c3a763: Obtain independent source delta review, regenerate new local pack/release bytes, rerun importer and consumer gates, then review the exact dev effect.
- db7650536375: Converge release metadata without changing archive bytes, prove a zero-diff replay, obtain independent dev-effect acceptance, and integrate into dev.
- 0c048b3baeb7: Replay the exact generator from clean HEAD, prove zero changed release files, then obtain independent dev-effect acceptance and integrate.

## Warnings

- None.

## Preview Caveat

- This draft is not an official release note and does not create tags or GitHub Releases.
