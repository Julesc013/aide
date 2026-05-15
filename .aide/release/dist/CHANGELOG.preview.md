# AIDE Changelog Preview

This file is generated from local Git history and is a preview only.

source_range: HEAD latest 50 commits
source_head: 2b2a00f7c462831170dc8de21834e1e5ec91708d
commit_count: 50
malformed_count: 15
preview_only: true
release_publishing: false

## Summary

- Added: 25
- Changed: 6
- Fixed: 8
- Docs: 3
- Tests: 5
- Internal: 10
- Risks: 1
- Follow-up: 1

## Added

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
- local release bundle generation is now evidenced for review only; no public release was created. (65a0c998d17d chore(release): generate local AIDE Lite bundle artifacts)
- Q48 release-draft queue packet and review-gated task registration. (8a6f1d8a646a policy(release): add Q48 GitHub release draft packet)
- Q48 release-draft policy, publication-boundary, upload-plan, checklist, and schema contracts. (82a09f910fe2 policy(release): define draft publication boundaries and checklists)
- AIDE Lite Q48 local release draft command surface and no-publish validation logic. (af9bb6b2ec53 feat(aide-lite): add GitHub release draft commands)
- Q48 release draft regression tests and golden task coverage for no-publish gates. (90ae50d9ce2b test(release): cover draft validation and no-publish gates)
- local-only GitHub Release draft generation artifacts and export-pack support for Q48. (abebc24278c5 chore(release): generate local GitHub release draft)
- stable pack, release, installability, and handoff checkpoint evidence. (2b2a00f7c462 audit(aide): checkpoint stable pack and installability)

## Changed

- refactor schemas now expose Q42 entry-level validation shapes. (76bbab2b2104 policy(refactor): define move salvage alias and rewrite rules)
- Q44 generated repair outputs now report no blockers for governance/test secret-handling references. (6ec097d8c421 chore(pack): export repair model support)
- Q44 queue index status now matches the Q44 task status. (73e58e4a741c policy(upgrade): add Q45 upgrade model packet)
- AIDE Lite selftest now uses representative golden-task smoke coverage instead of the full catalog. (fa35450ad44a perf(aide-lite): shorten selftest golden smoke)
- Golden-task report unit tests avoid repeated full-catalog report generation. (fa35450ad44a perf(aide-lite): shorten selftest golden smoke)
- Export-pack source lists now account for release support and exclude generated release outputs as target truth. (7a1cc9000953 feat(aide-lite): add release bundle and validation commands)

## Fixed

- Q41 status metadata now matches its needs_review task state. (88cd260b8fc0 policy(refactor): add Q42 map and alias planning packet)
- large text dependency scanning remains bounded while still detecting imports in AIDE Lite. (6ec097d8c421 chore(pack): export repair model support)
- Gateway unittest validation no longer times out under the previously failing command. (8c12de59f0e6 test(gateway): replace heavy skeleton fixture)
- AIDE Lite test/selftest validation is materially faster while full eval run remains exhaustive. (fa35450ad44a perf(aide-lite): shorten selftest golden smoke)
- Removed the stale generated-manifest warning from Harness validation. (0c1bd7437de0 chore(readiness): reconcile release warning state)
- Added missing Q45 upgrade golden task metadata directories already referenced by the catalog. (6ef828e53c15 test(release): cover archive generation and checksum validation)
- Release archives exclude forbidden local-state, secret-like, and raw prompt/response paths. (4f51d8ebde7a fix(release): exclude forbidden paths from local archives)
- Q47 no-publish golden now checks implementation primitives without false-positive matches on policy text. (e5a2692d3c45 fix(release): make no-publish golden ignore policy text)

## Docs

- describe Q43 install planning workflow and export boundary. (57ee11f988bb docs(install): document AIDE install planning model)
- recorded Q45 upgrade evidence and review-gate status. (ce1156a4f38a chore(pack): export upgrade model support)
- added Q48 GitHub Release draft workflow documentation. (1dacef0b00ef docs(release): document GitHub release draft workflow)

## Tests

- refreshed golden task run evidence for 85 deterministic tasks. (bf85d0313d21 chore(pack): export map and alias planning support)
- Q44 targeted repair tests and golden tasks are included in the pack. (6ec097d8c421 chore(pack): export repair model support)
- recorded upgrade validation, targeted unit tests, and residual gateway timeout. (ce1156a4f38a chore(pack): export upgrade model support)
- Gateway skeleton tests no longer run unrelated AIDE Lite report generation. (8c12de59f0e6 test(gateway): replace heavy skeleton fixture)
- Added release bundle archive, checksum, fixture extraction, and no-publish tests. (6ef828e53c15 test(release): cover archive generation and checksum validation)

## Internal

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
