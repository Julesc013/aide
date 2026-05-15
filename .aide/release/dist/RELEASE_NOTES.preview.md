# AIDE Release Notes Preview

This is a deterministic preview only. It does not publish a release.

source_range: HEAD latest 50 commits
source_head: 2b2a00f7c462831170dc8de21834e1e5ec91708d
preview_only: true

## Highlights

- Added: Q42 review-gated queue packet for candidate map and alias planning. (88cd260b8fc0)
- Added: Q42 candidate map, alias, rewrite, and draft ledger policy/schema layer. (76bbab2b2104)
- Added: preview-only Q42 map and alias command support. (9ec6fbd51729)
- Added: source-local candidate map artifacts as evidence, not target truth. (9ec6fbd51729)
- Added: Q42 no-apply map validation tests and golden tasks. (92edc034e194)
- Added: Q42 map/alias planning documentation and command references. (02796b275c3c)
- Added: Q44 repair policy and schema foundation. (90f2c1dfc34d)
- Added: portable repair/doctor model support in the AIDE Lite export pack. (6ec097d8c421)
- Added: Q45 upgrade model queue packet for no-apply upgrade planning work. (73e58e4a741c)
- Added: Q45 upgrade policy and schema foundation. (45678bb73b29)
- Added: portable rollback/uninstall policies, schemas, docs, tests, and AIDE Lite command support in the export pack. (99d1af6c5d40)
- Added: Recorded QFIX-05 warning inventory, validation, release-readiness audit, and remaining-risk evidence. (0c1bd7437de0)
- Added: Local release-bundle queue governance for aide-lite-pack-v0. (56ef5b86a00b)
- Added: Local release artifact and provenance policy contracts for aide-lite-pack-v0. (4b3f6de50825)
- Added: Release bundle schema records for archives, manifests, checksums, provenance, validation, reports, and install notes. (4b3f6de50825)
- Added: Local release bundle command surface for archive generation, checksum validation, fixture extraction, provenance, and dry-run cleanup. (7a1cc9000953)
- Added: Release bundle golden tasks for policy, schema, archive, checksum, extraction, no-publish, and forbidden path behavior. (6ef828e53c15)
- Added: Q47 local release bundle documentation and publication boundary guidance. (3b16f778e5b5)
- Added: local release bundle generation is now evidenced for review only; no public release was created. (65a0c998d17d)
- Added: Q48 release-draft queue packet and review-gated task registration. (8a6f1d8a646a)
- Added: Q48 release-draft policy, publication-boundary, upload-plan, checklist, and schema contracts. (82a09f910fe2)
- Added: AIDE Lite Q48 local release draft command surface and no-publish validation logic. (af9bb6b2ec53)
- Added: Q48 release draft regression tests and golden task coverage for no-publish gates. (90ae50d9ce2b)
- Added: local-only GitHub Release draft generation artifacts and export-pack support for Q48. (abebc24278c5)
- Added: stable pack, release, installability, and handoff checkpoint evidence. (2b2a00f7c462)
- Changed: refactor schemas now expose Q42 entry-level validation shapes. (76bbab2b2104)
- Changed: Q44 generated repair outputs now report no blockers for governance/test secret-handling references. (6ec097d8c421)
- Changed: Q44 queue index status now matches the Q44 task status. (73e58e4a741c)
- Changed: AIDE Lite selftest now uses representative golden-task smoke coverage instead of the full catalog. (fa35450ad44a)
- Changed: Golden-task report unit tests avoid repeated full-catalog report generation. (fa35450ad44a)
- Changed: Export-pack source lists now account for release support and exclude generated release outputs as target truth. (7a1cc9000953)
- Fixed: Q41 status metadata now matches its needs_review task state. (88cd260b8fc0)
- Fixed: large text dependency scanning remains bounded while still detecting imports in AIDE Lite. (6ec097d8c421)
- Fixed: Gateway unittest validation no longer times out under the previously failing command. (8c12de59f0e6)
- Fixed: AIDE Lite test/selftest validation is materially faster while full eval run remains exhaustive. (fa35450ad44a)
- Fixed: Removed the stale generated-manifest warning from Harness validation. (0c1bd7437de0)
- Fixed: Added missing Q45 upgrade golden task metadata directories already referenced by the catalog. (6ef828e53c15)
- Fixed: Release archives exclude forbidden local-state, secret-like, and raw prompt/response paths. (4f51d8ebde7a)
- Fixed: Q47 no-publish golden now checks implementation primitives without false-positive matches on policy text. (e5a2692d3c45)
- Docs: describe Q43 install planning workflow and export boundary. (57ee11f988bb)
- Docs: recorded Q45 upgrade evidence and review-gate status. (ce1156a4f38a)
- Docs: added Q48 GitHub Release draft workflow documentation. (1dacef0b00ef)
- Tests: refreshed golden task run evidence for 85 deterministic tasks. (bf85d0313d21)
- Tests: Q44 targeted repair tests and golden tasks are included in the pack. (6ec097d8c421)
- Tests: recorded upgrade validation, targeted unit tests, and residual gateway timeout. (ce1156a4f38a)
- Tests: Gateway skeleton tests no longer run unrelated AIDE Lite report generation. (8c12de59f0e6)
- Tests: Added release bundle archive, checksum, fixture extraction, and no-publish tests. (6ef828e53c15)

## Validation Summary

- 88cd260b8fc0: git diff --check: PASS.
- 88cd260b8fc0: git diff --check: PASS.
- 76bbab2b2104: git diff --check: PASS.
- 76bbab2b2104: git diff --check: PASS.
- 9ec6fbd51729: PASS: `git diff --check`
- 9ec6fbd51729: PASS: `git diff --check`
- 92edc034e194: PASS: `py -3 -m py_compile .aide/scripts/aide_lite.py`
- 02796b275c3c: PASS: `git diff --check`
- bf85d0313d21: PASS: `py -3 .aide/scripts/aide_lite.py refactor validate-map`.
- bf85d0313d21: PASS: `py -3 .aide/scripts/aide_lite.py refactor validate-map`.

## Known Risks

- 88cd260b8fc0: Q42 implementation is not complete in this commit; policy, command, test, docs, export, and final evidence commits follow.
- 88cd260b8fc0: Q42 implementation is not complete in this commit; policy, command, test, docs, export, and final evidence commits follow.
- 76bbab2b2104: Command implementation and generated current maps are not included yet.
- 76bbab2b2104: Command implementation and generated current maps are not included yet.
- 9ec6fbd51729: Candidate generation is intentionally conservative and sparse until a future reviewed task selects a concrete root or migration target.
- 9ec6fbd51729: Candidate generation is intentionally conservative and sparse until a future reviewed task selects a concrete root or migration target.
- 92edc034e194: Tests use deterministic fixtures and do not exercise target repositories.
- 02796b275c3c: Documentation describes only Q42 planning behavior; apply-capable install or migration behavior remains future work.
- bf85d0313d21: Core gateway unittest discovery still times out and needs separate investigation.
- bf85d0313d21: Core gateway unittest discovery still times out and needs separate investigation.

## Follow-up

- 88cd260b8fc0: Define Q42 map, salvage, alias, rewrite, and ledger policies and schemas.
- 88cd260b8fc0: Define Q42 map, salvage, alias, rewrite, and ledger policies and schemas.
- 76bbab2b2104: Add AIDE Lite refactor map commands and candidate output generation.
- 76bbab2b2104: Add AIDE Lite refactor map commands and candidate output generation.
- 9ec6fbd51729: Add Q42 unit and golden-task coverage.
- 9ec6fbd51729: Add Q42 unit and golden-task coverage.
- 92edc034e194: Document Q42 map planning workflow.
- 02796b275c3c: Export portable Q42 support and write final evidence.
- bf85d0313d21: Implement Q43 Install Plan Model v0 after Q42 review.
- bf85d0313d21: Implement Q43 Install Plan Model v0 after Q42 review.

## Warnings

- 15 malformed or legacy commits require review

## Preview Caveat

- This draft is not an official release note and does not create tags or GitHub Releases.
