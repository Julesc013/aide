# AIDE Changelog Preview

This file is generated from local Git history and is a preview only.

source_range: HEAD latest 50 commits
source_head: e5a2692d3c4593aaf9931b15adb55a201e703ce0
commit_count: 50
malformed_count: 15
preview_only: true
release_publishing: false

## Summary

- Added: 19
- Changed: 6
- Fixed: 11
- Docs: 4
- Tests: 6
- Internal: 15
- Risks: 1
- Follow-up: 1

## Added

- Q41 no-execution existing-tool absorption command surface and generated advisory tool outputs. (9e183cd9de4c feat(aide-lite): add tool inventory and wrap-plan commands)
- Q42 review-gated queue packet for candidate map and alias planning. (88cd260b8fc0 policy(refactor): add Q42 map and alias planning packet)
- Q42 candidate map, alias, rewrite, and draft ledger policy/schema layer. (76bbab2b2104 policy(refactor): define move salvage alias and rewrite rules)
- preview-only Q42 map and alias command support. (9ec6fbd51729 feat(aide-lite): add refactor map and alias commands)
- source-local candidate map artifacts as evidence, not target truth. (9ec6fbd51729 feat(aide-lite): add refactor map and alias commands)
- Q42 no-apply map validation tests and golden tasks. (92edc034e194 test(refactor): cover no-apply map validation)
- Q42 map/alias planning documentation and command references. (02796b275c3c docs(refactor): document move salvage and alias planning)
- Q44 repair policy and schema foundation. (90f2c1dfc34d policy(repair): define repair classes and safety gates)
- portable repair/doctor model support in the AIDE Lite export pack. (6ec097d8c421 chore(pack): export repair model support)
- Q45 upgrade model queue packet for no-apply upgrade planning work. (73e58e4a741c policy(upgrade): add Q45 upgrade model packet)
- Q45 upgrade policy and schema foundation. (45678bb73b29 policy(upgrade): define compatibility preservation and migration gates)
- portable rollback/uninstall policies, schemas, docs, tests, and AIDE Lite command support in the export pack. (99d1af6c5d40 chore(pack): export rollback and uninstall support)
- Recorded QFIX-05 warning inventory, validation, release-readiness audit, and remaining-risk evidence. (0c1bd7437de0 chore(readiness): reconcile release warning state)
- Local release-bundle queue governance for aide-lite-pack-v0. (56ef5b86a00b policy(release): add Q47 local bundle packet)
- Local release artifact and provenance policy contracts for aide-lite-pack-v0. (4b3f6de50825 policy(release): define local bundle artifacts and provenance)
- Release bundle schema records for archives, manifests, checksums, provenance, validation, reports, and install notes. (4b3f6de50825 policy(release): define local bundle artifacts and provenance)
- Local release bundle command surface for archive generation, checksum validation, fixture extraction, provenance, and dry-run cleanup. (7a1cc9000953 feat(aide-lite): add release bundle and validation commands)
- Release bundle golden tasks for policy, schema, archive, checksum, extraction, no-publish, and forbidden path behavior. (6ef828e53c15 test(release): cover archive generation and checksum validation)
- Q47 local release bundle documentation and publication boundary guidance. (3b16f778e5b5 docs(release): document AIDE Lite release bundle workflow)

## Changed

- refactor schemas now expose Q42 entry-level validation shapes. (76bbab2b2104 policy(refactor): define move salvage alias and rewrite rules)
- Q44 generated repair outputs now report no blockers for governance/test secret-handling references. (6ec097d8c421 chore(pack): export repair model support)
- Q44 queue index status now matches the Q44 task status. (73e58e4a741c policy(upgrade): add Q45 upgrade model packet)
- AIDE Lite selftest now uses representative golden-task smoke coverage instead of the full catalog. (fa35450ad44a perf(aide-lite): shorten selftest golden smoke)
- Golden-task report unit tests avoid repeated full-catalog report generation. (fa35450ad44a perf(aide-lite): shorten selftest golden smoke)
- Export-pack source lists now account for release support and exclude generated release outputs as target truth. (7a1cc9000953 feat(aide-lite): add release bundle and validation commands)

## Fixed

- export pack validation now includes the required Q38 mirrored ledger schema. (2cb95383f0ab fix(pack): restore quality schema export and selftest isolation)
- repo-intelligence fixture validation no longer depends on Q39 generated refactor outputs. (2cb95383f0ab fix(pack): restore quality schema export and selftest isolation)
- kept Q41 generated tool outputs out of Q37 repo-intelligence required-output validation. (bf27445fd62e chore(pack): export tool absorption support)
- Q41 status metadata now matches its needs_review task state. (88cd260b8fc0 policy(refactor): add Q42 map and alias planning packet)
- large text dependency scanning remains bounded while still detecting imports in AIDE Lite. (6ec097d8c421 chore(pack): export repair model support)
- Gateway unittest validation no longer times out under the previously failing command. (8c12de59f0e6 test(gateway): replace heavy skeleton fixture)
- AIDE Lite test/selftest validation is materially faster while full eval run remains exhaustive. (fa35450ad44a perf(aide-lite): shorten selftest golden smoke)
- Removed the stale generated-manifest warning from Harness validation. (0c1bd7437de0 chore(readiness): reconcile release warning state)
- Added missing Q45 upgrade golden task metadata directories already referenced by the catalog. (6ef828e53c15 test(release): cover archive generation and checksum validation)
- Release archives exclude forbidden local-state, secret-like, and raw prompt/response paths. (4f51d8ebde7a fix(release): exclude forbidden paths from local archives)
- Q47 no-publish golden now checks implementation primitives without false-positive matches on policy text. (e5a2692d3c45 fix(release): make no-publish golden ignore policy text)

## Docs

- Q40 evidence counts now match the final rebased tree. (087907637fb0 chore(sync): refresh generated refs after commit rewrite)
- Q41 is documented as no-execution, no-delete, no-rename, no-migration tool absorption planning infrastructure. (7ea3b9b6676d docs(tools): document existing tool absorption)
- describe Q43 install planning workflow and export boundary. (57ee11f988bb docs(install): document AIDE install planning model)
- recorded Q45 upgrade evidence and review-gate status. (ce1156a4f38a chore(pack): export upgrade model support)

## Tests

- Q41 now has deterministic no-call regression coverage for tool absorption behavior. (5293a1c3a9ae test(tools): cover tool classification and no-execution gates)
- refreshed golden task run evidence for 85 deterministic tasks. (bf85d0313d21 chore(pack): export map and alias planning support)
- Q44 targeted repair tests and golden tasks are included in the pack. (6ec097d8c421 chore(pack): export repair model support)
- recorded upgrade validation, targeted unit tests, and residual gateway timeout. (ce1156a4f38a chore(pack): export upgrade model support)
- Gateway skeleton tests no longer run unrelated AIDE Lite report generation. (8c12de59f0e6 test(gateway): replace heavy skeleton fixture)
- Added release bundle archive, checksum, fixture extraction, and no-publish tests. (6ef828e53c15 test(release): cover archive generation and checksum validation)

## Internal

- refreshed generated root references after local commit-message repair. (087907637fb0 chore(sync): refresh generated refs after commit rewrite)
- regenerated export-pack metadata and payload after the helper fix. (2cb95383f0ab fix(pack): restore quality schema export and selftest isolation)
- added Q41 Existing Tool Absorption v0 as an in-progress no-execution tool absorption phase. (9c06ac935011 policy(tools): add Q41 existing tool absorption packet)
- introduced the Q41 no-execution tool absorption contract and schema substrate. (d5efd07ff33d policy(tools): define tool fates capabilities and risks)
- exported Q41 existing-tool absorption support in the AIDE Lite portable pack. (bf27445fd62e chore(pack): export tool absorption support)
- exported Q42 move-map, salvage-map, path-alias, reference-rewrite, and migration-ledger planning support. (bf85d0313d21 chore(pack): export map and alias planning support)
- export Q43 install planning support and evidence. (85442fe952ef chore(pack): export install planning support)
- add Q44 repair/doctor queue packet and evidence scaffold. (df2c80556ca7 policy(repair): add Q44 repair doctor packet)
- No command surface or generated upgrade output is added in this commit. (45678bb73b29 policy(upgrade): define compatibility preservation and migration gates)
- exported Q45 upgrade planning support in the AIDE Lite pack. (ce1156a4f38a chore(pack): export upgrade model support)
- added the Q46 queue control packet for rollback/uninstall planning. (9dbc9e6f7618 policy(rollback): add Q46 rollback uninstall packet)
- Q46 evidence records no-apply status, pack boundary checks, and residual validation risks. (99d1af6c5d40 chore(pack): export rollback and uninstall support)
- synchronized local `main` with the remote-only Q43 documentation commit before push. (8bbe3a9329c4 chore(sync): merge origin main before push)
- Gateway test fixtures remain deterministic and provider/model/network-call free. (8c12de59f0e6 test(gateway): replace heavy skeleton fixture)
- Export pack carries the optimized AIDE Lite script and test updates. (fa35450ad44a perf(aide-lite): shorten selftest golden smoke)

## Risks

- Immediate public release remains blocked by review gates and future Q47/Q48 release work. (0c1bd7437de0 chore(readiness): reconcile release warning state)

## Follow-up

- Q43 Install Plan Model v0 can consume candidate map planning references. (bf85d0313d21 chore(pack): export map and alias planning support)

## Malformed Commits

- 894cba91a3d6 policy(install): add Q43 install planning packet: missing_changelog_category
- f90a2800c383 policy(install): define preservation ownership and conflicts: missing_changelog_category
- ef8c59688760 feat(aide-lite): add install observe plan and dry-run commands: missing_changelog_category
- 327d594ada86 test(install): cover no-apply install planning: missing_changelog_category
- 360b5544f7fd docs(install): document AIDE install planning model: missing_changelog_category
- e3b8ecfc08c2 feat(aide-lite): add repair observe plan and dry-run commands: missing_changelog_category
- 34608d2305fa test(repair): cover no-apply repair planning: missing_changelog_category
- ce80ac84b296 docs(repair): document AIDE repair doctor model: missing_changelog_category
- de8a6a061580 feat(aide-lite): add upgrade observe compare plan and dry-run commands: missing_changelog_category
- 8139b931f37a test(upgrade): cover no-apply upgrade planning: missing_changelog_category
- 016f8126aecf docs(upgrade): document AIDE upgrade model: missing_changelog_category
- a7ed9e6f0f3e policy(rollback): define rollback and uninstall preservation gates: missing_changelog_category
- c083e1bccf6b feat(aide-lite): add rollback and uninstall planning commands: missing_changelog_category
- c5a320208857 test(rollback): cover no-apply rollback and uninstall planning: missing_changelog_category
- d587005acbfa docs(rollback): document rollback and uninstall model: missing_changelog_category

## Release Caveat

- Preview only. No tags, GitHub Releases, branch mutation, or publishing were performed.
