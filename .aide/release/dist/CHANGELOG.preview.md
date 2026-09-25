# AIDE Changelog Preview

This file is generated from local Git history and is a preview only.

source_range: HEAD latest 50 commits
source_head: 49318d50472b17f648c2f29e998239b9c446cf14
commit_count: 50
malformed_count: 0
preview_only: true
release_publishing: false

## Summary

- Added: 3
- Fixed: 3
- Internal: 44

## Added

- restore a missing receipt-owned file from the exact delivered pack. (49f38d12f425 feat(import): repair one missing receipt-owned file)
- receipt-backed read-only removal planning in the delivered portable CLI. (1a25e33effc5 feat(pack): integrate receipt-bound removal planning)
- conditional receipt-owned removal apply for exact generated material. (d13894ba0f55 feat(uninstall): detach exact generated files and retire receipt)

## Fixed

- receipt-owned removal recovery preserves later authored bytes and retains ownership evidence when a recorded path was already absent. (fbd9465344f0 fix(removal): bind recovery intents to receipt-owned bytes)
- Generated install guidance now describes the supported bounded removal apply path. (597b5bcd6f54 fix(release): describe bounded removal apply in install guides)
- Generated removal guidance now describes planner output and recovery states accurately. (49318d50472b fix(release): clarify removal planner and recovery guidance)

## Internal

- align historical dev integration records with completed technical checks. (5ac617b37b57 chore(queue): close historical dev integration evidence)
- record source integration without claiming lifecycle or release acceptance. (fce11e7fce3e chore(queue): record observed historical dev integration)
- route reviewed host source through a bounded dev integration task. (526e9e402c56 chore(queue): admit isolated-host API query dev integration)
- combine isolated-host API-query source without native or hosted activation. (ab17fd664159 feat(runtime): integrate reviewed API query source with dev)
- align local portable and release preview bytes with combined host source. (3875cad7af78 build(release): refresh host source portable projection)
- stabilize local source-ancestor release metadata. (a4ee0f32ec7e fix(release): record stable host source ancestor metadata)
- align host integration evidence with frozen local artifacts. (a55b804bb573 chore(queue): close host integration review evidence)
- record isolated-host source integration with operational gates retained. (1c75abf1d93b chore(queue): record observed host source dev integration)
- route removal planner through a bounded current-dev integration. (7bc4c9b5087b chore(queue): admit removal planner dev integration)
- materialize the combined portable and local release projection. (9c284081fc33 build(pack): materialize combined removal-planner artifacts)
- bind local release metadata to the combined source and artifact lineage. (2819385a5b3d build(release): bind combined removal artifacts to ancestry)
- close review evidence for the removal-planner dev candidate. (ae0e29e98eb4 docs(queue): record reviewed removal integration candidate)
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

## Malformed Commits

- None.

## Release Caveat

- Preview only. No tags, GitHub Releases, branch mutation, or publishing were performed.
