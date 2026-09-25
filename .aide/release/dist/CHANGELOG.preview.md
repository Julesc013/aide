# AIDE Changelog Preview

This file is generated from local Git history and is a preview only.

source_range: HEAD latest 50 commits
source_head: 8365aa61b7cad51d542f88434e50bc33c5aac8fe
commit_count: 50
malformed_count: 0
preview_only: true
release_publishing: false

## Summary

- Added: 7
- Changed: 9
- Fixed: 11
- Security: 1
- Internal: 23

## Added

- conditional receipt-owned removal apply for exact generated material. (d13894ba0f55 feat(uninstall): detach exact generated files and retire receipt)
- bounded predecessor-pack rollback apply for the declared Windows slice. (23422130fcfc feat(rollback): apply exact predecessor portable pack)
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

- receipt-owned removal recovery preserves later authored bytes and retains ownership evidence when a recorded path was already absent. (fbd9465344f0 fix(removal): bind recovery intents to receipt-owned bytes)
- Generated install guidance now describes the supported bounded removal apply path. (597b5bcd6f54 fix(release): describe bounded removal apply in install guides)
- Generated removal guidance now describes planner output and recovery states accurately. (49318d50472b fix(release): clarify removal planner and recovery guidance)
- authored AGENTS backup recovery retains receipt and intent until exact original backup cleanup is reconciled. (2c4c9089a546 fix(removal): reconcile authored AGENTS backup before receipt retirement)
- Pending portable removal now blocks exact-predecessor rollback preview and apply. (1f920ebbf7bf fix(rollback): block rollback while removal recovery is pending)
- Exact predecessor rollback now accepts an unchanged authored CRLF AGENTS.md managed section. (9a0843c3a763 fix(lifecycle): accept exact CRLF managed section in rollback)
- Missing receipt-owned files now conflict instead of being silently recreated. (acbcb9c8bd62 feat(update): preserve project choices across successive packs)
- Receipt-owned CRLF AGENTS sections update when their upstream managed block changes. (3239530132a6 fix(update): preserve receipt-owned CRLF managed sections)
- Automatic managed updates now require a validated predecessor baseline instead of a local receipt claim alone. (12758e07373f fix(update): bind owned updates to the validated predecessor)
- Reject receipt claims that disagree with the delivered pack during installed health inspection. (486aa2bd0f5f fix(repair): bind health receipt rows to pack baseline)
- Recognize valid CRLF portable guidance blocks during read-only installed health inspection. (558638203fae fix(repair): preserve raw CRLF pack block identity)

## Security

- Rollback no longer accepts a checksum-valid payload through a reparse pack boundary. (33824b369b84 fix(rollback): reject reparse pack roots before rollback)

## Internal

- record exact repair staging dev-integration readiness. (10a16afb681e docs(queue): record repair staging zero-change replay)
- record accepted Windows repair staging in remote dev. (6377cda923c1 docs(queue): record remote dev repair staging integration)
- construct current-dev safe importer integration candidate. (7624d9f4b542 fix(import): combine reviewed Windows importer writes with dev)
- bind safe importer portable assets to the reviewed combined source. (0fbabcdd8510 chore(import): project reviewed safe importer artifacts)
- converge safe importer artifact metadata after projection. (515ad6b2c07e chore(import): converge safe importer release metadata)
- close the bounded safe importer integration gate. (5317524f0760 chore(import): close safe importer dev integration record)
- construct conditional removal integration candidate. (009668559436 fix(removal): combine reviewed conditional detach with dev)
- durable campaign continuation checkpoint. (b05ba7d5984f chore(campaign): checkpoint delivery after owner window)
- Local review-ready removal artifacts and evidence are projected from the corrected source. (704825d14643 chore(release): project reviewed removal artifact bytes)
- Converged release metadata for reviewed local removal artifacts. (7b23b71912ba chore(release): converge removal metadata after projection)
- Preserve dev checkpoint ancestry in the removal integration candidate. (a60b8cb01106 chore(campaign): retain dev checkpoint in removal candidate)
- Durable dev checkpoint and remaining owned-section removal obligation. (ea53e319bd06 chore(campaign): record removal dev checkpoint and open section work)
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

## Malformed Commits

- None.

## Release Caveat

- Preview only. No tags, GitHub Releases, branch mutation, or publishing were performed.
