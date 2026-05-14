# AIDE Release Notes Preview

This is a deterministic preview only. It does not publish a release.

source_range: HEAD latest 50 commits
source_head: e5a2692d3c4593aaf9931b15adb55a201e703ce0
preview_only: true

## Highlights

- Added: Q41 no-execution existing-tool absorption command surface and generated advisory tool outputs. (9e183cd9de4c)
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
- Changed: refactor schemas now expose Q42 entry-level validation shapes. (76bbab2b2104)
- Changed: Q44 generated repair outputs now report no blockers for governance/test secret-handling references. (6ec097d8c421)
- Changed: Q44 queue index status now matches the Q44 task status. (73e58e4a741c)
- Changed: AIDE Lite selftest now uses representative golden-task smoke coverage instead of the full catalog. (fa35450ad44a)
- Changed: Golden-task report unit tests avoid repeated full-catalog report generation. (fa35450ad44a)
- Changed: Export-pack source lists now account for release support and exclude generated release outputs as target truth. (7a1cc9000953)
- Fixed: export pack validation now includes the required Q38 mirrored ledger schema. (2cb95383f0ab)
- Fixed: repo-intelligence fixture validation no longer depends on Q39 generated refactor outputs. (2cb95383f0ab)
- Fixed: kept Q41 generated tool outputs out of Q37 repo-intelligence required-output validation. (bf27445fd62e)
- Fixed: Q41 status metadata now matches its needs_review task state. (88cd260b8fc0)
- Fixed: large text dependency scanning remains bounded while still detecting imports in AIDE Lite. (6ec097d8c421)
- Fixed: Gateway unittest validation no longer times out under the previously failing command. (8c12de59f0e6)
- Fixed: AIDE Lite test/selftest validation is materially faster while full eval run remains exhaustive. (fa35450ad44a)
- Fixed: Removed the stale generated-manifest warning from Harness validation. (0c1bd7437de0)
- Fixed: Added missing Q45 upgrade golden task metadata directories already referenced by the catalog. (6ef828e53c15)
- Fixed: Release archives exclude forbidden local-state, secret-like, and raw prompt/response paths. (4f51d8ebde7a)
- Fixed: Q47 no-publish golden now checks implementation primitives without false-positive matches on policy text. (e5a2692d3c45)
- Docs: Q40 evidence counts now match the final rebased tree. (087907637fb0)
- Docs: Q41 is documented as no-execution, no-delete, no-rename, no-migration tool absorption planning infrastructure. (7ea3b9b6676d)
- Docs: describe Q43 install planning workflow and export boundary. (57ee11f988bb)
- Docs: recorded Q45 upgrade evidence and review-gate status. (ce1156a4f38a)
- Tests: Q41 now has deterministic no-call regression coverage for tool absorption behavior. (5293a1c3a9ae)
- Tests: refreshed golden task run evidence for 85 deterministic tasks. (bf85d0313d21)
- Tests: Q44 targeted repair tests and golden tasks are included in the pack. (6ec097d8c421)
- Tests: recorded upgrade validation, targeted unit tests, and residual gateway timeout. (ce1156a4f38a)
- Tests: Gateway skeleton tests no longer run unrelated AIDE Lite report generation. (8c12de59f0e6)
- Tests: Added release bundle archive, checksum, fixture extraction, and no-publish tests. (6ef828e53c15)

## Validation Summary

- 087907637fb0: `py -3 .aide/scripts/aide_lite.py roots inventory`: PASS.
- 087907637fb0: `py -3 .aide/scripts/aide_lite.py roots inventory`: PASS.
- 2cb95383f0ab: `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0`: PASS.
- 2cb95383f0ab: `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0`: PASS.
- 2cb95383f0ab: `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0`: PASS.
- 9c06ac935011: git diff --check: PASS.
- d5efd07ff33d: py -3 -c JSON schema load check: PASS.
- 9e183cd9de4c: py -3 -m py_compile .aide/scripts/aide_lite.py: PASS.
- 5293a1c3a9ae: py -3 -m unittest discover -s .aide/scripts/tests -p test_q41_tool_absorption.py: PASS.
- 7ea3b9b6676d: git diff --check: PASS.

## Known Risks

- 087907637fb0: Generated source references point to the parent commit by design because the artifact commit itself cannot include its own final hash.
- 087907637fb0: Generated source references point to the parent commit by design because the artifact commit itself cannot include its own final hash.
- 2cb95383f0ab: Full direct unittest discovery exceeded the local timeout; targeted suites and AIDE Lite selftest/test passed.
- 2cb95383f0ab: Full direct unittest discovery exceeded the local timeout; targeted suites and AIDE Lite selftest/test passed.
- 2cb95383f0ab: Full direct unittest discovery exceeded the local timeout; targeted suites and AIDE Lite selftest/test passed.
- 9c06ac935011: Evidence is scaffolded and will be completed after implementation and validation.
- d5efd07ff33d: Policies and schemas are advisory until command support and validation are wired in the next commit.
- 9e183cd9de4c: Tool detection remains deterministic and heuristic; target repos must generate their own inventories before any future wrapper work.
- 5293a1c3a9ae: Coverage uses fixture heuristics and does not prove semantic correctness of every target-repo tool system.
- 7ea3b9b6676d: Documentation intentionally does not claim concrete Dominium or Eureka tool absorption is complete.

## Follow-up

- 087907637fb0: Run final validation and push `main` to `origin/main` as a fast-forward.
- 087907637fb0: Run final validation and push `main` to `origin/main` as a fast-forward.
- 2cb95383f0ab: Push the rebased `main` to `origin/main` and verify local and remote refs match.
- 2cb95383f0ab: Push the rebased `main` to `origin/main` and verify local and remote refs match.
- 2cb95383f0ab: Push the rebased `main` to `origin/main` and verify local and remote refs match.
- 9c06ac935011: Define tool absorption policies, schemas, commands, tests, docs, export-pack support, and final evidence.
- d5efd07ff33d: Add deterministic AIDE Lite tools commands and generated tool absorption outputs.
- 9e183cd9de4c: Add golden tasks, unittest coverage, docs, export-pack sync, and final evidence.
- 5293a1c3a9ae: Update documentation, command catalog, export pack, generated Q42 task packet, and final evidence.
- 7ea3b9b6676d: Export Q41 portable files, regenerate Q42 task packet, write final evidence, and run full validation.

## Warnings

- 15 malformed or legacy commits require review

## Preview Caveat

- This draft is not an official release note and does not create tags or GitHub Releases.
