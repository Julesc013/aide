# AIDE Changelog Preview

This file is generated from local Git history and is a preview only.

source_range: HEAD latest 50 commits
source_head: 9a0843c3a7633002f91a0ec3e707fe613650eb5f
commit_count: 50
malformed_count: 0
preview_only: true
release_publishing: false

## Summary

- Added: 3
- Fixed: 6
- Security: 1
- Internal: 40

## Added

- conditional receipt-owned removal apply for exact generated material. (d13894ba0f55 feat(uninstall): detach exact generated files and retire receipt)
- bounded predecessor-pack rollback apply for the declared Windows slice. (23422130fcfc feat(rollback): apply exact predecessor portable pack)
- receipt-owned managed-section removal inside authored AGENTS.md on Windows, preserving all outside bytes. (d5b44626d6f9 feat(removal): detach owned AGENTS section in brownfield projects)

## Fixed

- receipt-owned removal recovery preserves later authored bytes and retains ownership evidence when a recorded path was already absent. (fbd9465344f0 fix(removal): bind recovery intents to receipt-owned bytes)
- Generated install guidance now describes the supported bounded removal apply path. (597b5bcd6f54 fix(release): describe bounded removal apply in install guides)
- Generated removal guidance now describes planner output and recovery states accurately. (49318d50472b fix(release): clarify removal planner and recovery guidance)
- authored AGENTS backup recovery retains receipt and intent until exact original backup cleanup is reconciled. (2c4c9089a546 fix(removal): reconcile authored AGENTS backup before receipt retirement)
- Pending portable removal now blocks exact-predecessor rollback preview and apply. (1f920ebbf7bf fix(rollback): block rollback while removal recovery is pending)
- Exact predecessor rollback now accepts an unchanged authored CRLF AGENTS.md managed section. (9a0843c3a763 fix(lifecycle): accept exact CRLF managed section in rollback)

## Security

- Rollback no longer accepts a checksum-valid payload through a reparse pack boundary. (33824b369b84 fix(rollback): reject reparse pack roots before rollback)

## Internal

- close observed dev integration of receipt-backed removal planning. (5dfa75e632b0 docs(queue): record removal planner on remote dev)
- route importer parent-substitution safety through a bounded implementation task. (f3e668513975 chore(queue): admit safe delivered-pack importer writes)
- preserve a failing importer parent-substitution oracle before repair. (26720ed197d0 test(pack): reproduce importer parent-junction escape)
- preserve effect-time ownership regressions before importer repair. (e7c320cb8ec9 test(pack): reproduce importer concurrent-leaf clobber)
- track the mandatory removal apply implementation separately from planning. (b2d159aa6c48 chore(queue): admit receipt-owned removal apply)
- preserve the importer intent parent-race oracle before repair. (f34947f6a78b test(pack): reproduce importer intent parent escape)
- close reviewed ownership and path-race defects for one missing receipt-owned file. (52b338eef8ff fix(pack): serialize repair and import effects with pinned paths)
- document the narrow safety contract for subsequent source repair. (01466f9e1814 docs(pack): record importer write safety invariants)
- preserve a tested partial owned-removal source checkpoint. (cd636c9ccd0d feat(pack): checkpoint partial receipt-owned removal apply)
- make the partial lifecycle checkpoint restartable and honest. (ed366600dbc1 docs(queue): record partial removal source checkpoint)
- protect repair-intent cleanup from outside-target deletion. (45c5ce91132a fix(pack): delete repair intents through verified Windows handles)
- close the owned repair source review for dev integration. (cdb3bd04f1ae docs(queue): record accepted owned repair source review)
- plan reviewed repair integration with current dev. (d40c18ccc744 chore(queue): admit owned repair dev integration)
- integrate one receipt-owned missing-file repair with delivered removal planning. (71501c6bb30b feat(pack): integrate reviewed owned repair with removal planner)
- refresh local portable release candidates after owned repair source merge. (ef60c1388ee5 build(release): project combined owned repair artifacts)
- repair integration scope metadata. (3ed628c19aed fix(queue): align owned repair integration allowlist)
- converge local release metadata after committed source projection. (e4697aaa3271 build(release): converge owned repair release projection)
- close the combined owned repair source and local artifact review for dev integration. (6b4007d06546 docs(queue): record accepted owned repair integration)
- preserve integration effect and newly discovered safety blocker. (9a8b08700ef7 docs(queue): record owned repair dev effect and new race)
- track repair publication safety fix forward. (fdad1a06f3fe chore(queue): admit Windows repair staging hardening)
- harden owned repair publication against competing Windows writers. (1a44ec617508 fix(repair): deny competing writes to Windows repair staging)
- close the repair staging setup-failure leak found in review. (e215698a993d fix(repair): clean exclusive stage after descriptor setup errors)
- harden delivered-pack Windows import writes and recovery evidence. (0dfb2931d32f fix(import): anchor Windows importer writes and guard stages)
- bind exclusive Windows repair staging to current local delivery artifacts. (d4311651b76d build(release): project repaired Windows staging source into local pack)
- converge release provenance for the reviewed Windows repair staging source. (9f2f38957e57 build(release): converge repair staging source ancestry metadata)
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

## Malformed Commits

- None.

## Release Caveat

- Preview only. No tags, GitHub Releases, branch mutation, or publishing were performed.
