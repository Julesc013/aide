# AIDE Changelog Preview

This file is generated from local Git history and is a preview only.

source_range: HEAD latest 50 commits
source_head: 0509e1611b1838c650954c64212ad603f132dada
commit_count: 50
malformed_count: 0
preview_only: true
release_publishing: false

## Summary

- Added: 5
- Changed: 9
- Fixed: 13
- Security: 1
- Internal: 23

## Added

- receipt-owned managed-section removal inside authored AGENTS.md on Windows, preserving all outside bytes. (d5b44626d6f9 feat(removal): detach owned AGENTS section in brownfield projects)
- Local delivered pack evidence for supported rollback, owned removal, and interruption recovery. (db7650536375 chore(lifecycle): project reviewed lifecycle source into local pack)
- Bounded plan for manual portable-pack conflict resolution and disabled-feature preservation. (63484c756197 chore(update): admit bounded successive project update task)
- Manual three-way portable-pack resolution and explicit optional-example disable survival. (acbcb9c8bd62 feat(update): preserve project choices across successive packs)
- Inspect the health of a delivered Lite installation without modifying its target. (03c5e7f81c22 feat(repair): inspect installed Lite pack health)

## Changed

- Local release provenance now records clean ancestor status for the lifecycle pack. (0c048b3baeb7 chore(lifecycle): converge local release metadata after projection)
- Recorded local lifecycle release replay evidence. (7e8816b60af7 chore(lifecycle): record zero-diff release replay evidence)
- Recorded completed lifecycle dev integration evidence and next mandatory product gap. (d4b67c96ff81 chore(lifecycle): record observed dev integration and close task)
- Track installed Lite repair diagnosis as a bounded campaign task. (0aa5a9d23b10 chore(repair): admit installed Lite health diagnosis task)
- Keep predecessor-bound import and rollback regressions aligned with the validated receipt contract. (c68077548ee9 test(import): bind legacy update and rollback oracles)
- Combine delivered update and read-only repair-health implementation for qualification. (99a9e54da887 chore(campaign): combine update and repair health candidates)
- Track the bounded stable release contract as a campaign WorkUnit. (74093ecacb4f chore(release): admit stable contract WorkUnit)
- Define a reviewable candidate for the first stable Lite release contract. (aa3bcfec849e chore(release): define stable Lite contract candidate)
- Refresh local portable-pack and release-preview outputs for qualified combined source. (d137f936bf0a chore(pack): refresh combined update and health previews)

## Fixed

- authored AGENTS backup recovery retains receipt and intent until exact original backup cleanup is reconciled. (2c4c9089a546 fix(removal): reconcile authored AGENTS backup before receipt retirement)
- Pending portable removal now blocks exact-predecessor rollback preview and apply. (1f920ebbf7bf fix(rollback): block rollback while removal recovery is pending)
- Exact predecessor rollback now accepts an unchanged authored CRLF AGENTS.md managed section. (9a0843c3a763 fix(lifecycle): accept exact CRLF managed section in rollback)
- Missing receipt-owned files now conflict instead of being silently recreated. (acbcb9c8bd62 feat(update): preserve project choices across successive packs)
- Receipt-owned CRLF AGENTS sections update when their upstream managed block changes. (3239530132a6 fix(update): preserve receipt-owned CRLF managed sections)
- Automatic managed updates now require a validated predecessor baseline instead of a local receipt claim alone. (12758e07373f fix(update): bind owned updates to the validated predecessor)
- Reject receipt claims that disagree with the delivered pack during installed health inspection. (486aa2bd0f5f fix(repair): bind health receipt rows to pack baseline)
- Recognize valid CRLF portable guidance blocks during read-only installed health inspection. (558638203fae fix(repair): preserve raw CRLF pack block identity)
- installed Lite Task OS reports no selected task for an empty queue. (f00d937e2368 fix(task-os): keep empty target queue reports truthful)
- project-owned Lite target queues no longer receive AIDE source-phase next-work advice. (e88a1468acd2 fix(task-os): keep target queue next work project-owned)
- target Task OS routing follows its declared profile even when a queue ID matches an AIDE source task. (b9d2b150c39c fix(task-os): route target next work by declared profile)
- target next-work explanation remains accurate even when queue IDs collide with source IDs. (52e1f194ebd2 fix(task-os): keep copied-id target reason truthful)
- local draft lifecycle claims now match the bounded Windows apply candidates. (bc1867a06933 fix(release): distinguish lifecycle planners from bounded apply)

## Security

- Rollback no longer accepts a checksum-valid payload through a reparse pack boundary. (33824b369b84 fix(rollback): reject reparse pack roots before rollback)

## Internal

- Record the combined delivered-pack lifecycle qualification task. (f2be45ea13ce chore(lifecycle): admit combined portable integration task)
- Preserve rollback ancestry for combined lifecycle qualification. (03f4b0a1ef37 chore(lifecycle): retain reviewed rollback source in combined candidate)
- Preserve accepted removal source for combined lifecycle qualification. (723322cf07ab chore(lifecycle): retain reviewed removal source in combined candidate)
- Converge local release metadata after the reviewed artifact projection. (54b9d45eeaa3 chore(pack): converge preview metadata after projection)
- Close the bounded update and repair-health dev integration record. (a32535a2675f chore(queue): close combined update and health dev integration)
- Merge current dev history for contract repair without declaring public release behavior. (060de47208b3 chore(release): merge current dev into stable contract task)
- Correct the proposed first stable Lite release contract and its review evidence. (4315a8130db2 fix(release): repair stable Lite contract review findings)
- Correct contract review provenance without changing policy or implementation bytes. (d38e5839fe10 chore(release): bind contract evidence to repaired source hashes)
- Route contract projection through its own bounded WorkUnit. (7168ee1cfaa8 chore(queue): admit stable contract artifact projection)
- Preserve exact contract evidence ancestry in projection history. (d3d9848569a9 chore(release): merge corrected contract evidence into projection)
- Record accepted source dependency for bounded projection. (8365aa61b7ca chore(release): bind accepted contract source to projection)
- Refresh local preview artifacts for the accepted Lite contract. (d0bfa4045a3c chore(release): project accepted Lite contract into preview assets)
- Converge local preview release metadata without rebuilding archives. (2defcad541d0 chore(release): converge Lite contract preview metadata)
- Close the bounded stable contract source and local-preview dev integration records. (b3a001befaac chore(queue): close stable Lite contract dev integration)
- Route mandatory delivered Lite consumer checks through a bounded WorkUnit. (5561aecdb608 chore(queue): admit delivered Lite consumer prequalification)
- preserve bounded local consumer evidence and a reproducible Task OS repair trigger. (b45010280e5e test(lite): record delivered consumer prequalification)
- create a bounded route for evidence-only dev integration. (736e3f9ac027 chore(queue): admit Lite evidence dev integration)
- complete a separate evidence-only dev integration review packet. (a7254d7d4c9c chore(queue): freeze Lite evidence integration packet)
- preserve verified Windows Lite preview evidence integration and unresolved release gates. (d292253b0994 chore(lite): close observed consumer evidence dev effect)
- preserve independent Task OS source review and its release-blocking follow-up. (04caefe65986 chore(task-os): record exact empty-queue source review)
- preserve the exact Task OS repaired-source review result. (75406123ccb0 chore(task-os): preserve accepted target routing review)
- preserve exact Q48 source review and remaining gates. (59286688dfce chore(release): preserve accepted draft source review)
- admit current Lite preview projection and qualification task. (0509e1611b18 chore(release): admit current Lite artifact projection)

## Malformed Commits

- None.

## Release Caveat

- Preview only. No tags, GitHub Releases, branch mutation, or publishing were performed.
