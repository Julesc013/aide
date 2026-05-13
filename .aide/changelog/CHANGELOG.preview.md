# AIDE Changelog Preview

This file is generated from local Git history and is a preview only.

source_range: HEAD latest 50 commits
source_head: 6246811cf02ece09bd25b53ce0625919db658f51
commit_count: 50
malformed_count: 8
preview_only: true
release_publishing: false

## Summary

- Added: 9
- Changed: 8
- Fixed: 9
- Docs: 8
- Tests: 14
- Internal: 32
- Risks: 9
- Follow-up: 5

## Added

- canonical AIDE commit discipline and WorkUnit recovery policy. (86974c90938c policy(aide): define structured commits and WorkUnit recovery)
- AIDE Lite commit, changelog, and task recovery command surfaces. (2146efa0db8f feat(aide-lite): add commit and task recovery commands)
- canonical Git workflow policy files for branch roles, promotion gates, sync posture, prune posture, and project profiles. (5cb6dea4fb4c policy(git): define branch roles and promotion rules)
- report-only Git workflow detection and branch-role command surface. (f4b8347da2be feat(aide-lite): add report-only Git workflow detection)
- dry-run Git helper command surface for local branch planning, landing, promotion, sync, and prune guards. (8fc3bfe63dcd feat(git): add dry-run branch helper commands)
- Q34 release draft governance queue packet for preview-only changelog and release-note generation. (2471b73deb67 policy(changelog): add Q34 release draft governance packet)
- preview-only changelog and release-note generator command surface. (52afde5b0161 feat(changelog): generate changelog and release-note previews)
- changelog policy, config, templates, release-notes JSON, and latest report support. (52afde5b0161 feat(changelog): generate changelog and release-note previews)
- Generated preview-only changelog and release-note draft artifacts for Q34 review. (e0606831f7a9 chore(pack): export changelog preview support)

## Changed

- WorkUnit recovery preflight now includes branch-role inspection. (5cb6dea4fb4c policy(git): define branch roles and promotion rules)
- updated next-phase guidance from Q28 redo to Q29 merge/land/promote helpers. (c305b581855a docs(git): document AIDE branch workflow policy)
- Q28 queue state now stops at needs_review with complete evidence. (0fb6bb2872d7 chore(pack): export Git workflow policies)
- safe import now treats portable docs/reference governance docs as target-safe. (802052185200 policy(pack): include commit recovery and Git workflow files)
- Updated agent guidance for target sync and adapter-generated guidance inputs. (62d13ad71795 docs(pack): document portable governance sync)
- export/import policy now names portable changelog policy and templates. (52afde5b0161 feat(changelog): generate changelog and release-note previews)
- Command catalog now lists changelog preview/validate/status. (453fe6aa9d66 docs(changelog): document release draft workflow)
- eval reports now use an explicit token budget. (6246811cf02e fix(recovery): clear remaining validation warnings)

## Fixed

- made task inspection resolve compact short task ids through the queue index. (600c5fb2e61b chore(pack): export commit and recovery policies)
- AIDE Lite selftest fixture now includes Q28 policy files when Q28 golden tasks run. (0fb6bb2872d7 chore(pack): export Git workflow policies)
- excluded AIDE-local Q30 branch-policy artifacts from portable pack truth. (0e62caef186f chore(pack): export updated Git workflow policy)
- imported target Git policy no longer fails solely because target-local helper plans have not been generated yet. (802052185200 policy(pack): include commit recovery and Git workflow files)
- Q31 governance validation no longer rejects target-style repos that do not contain a source export pack. (7119f14dbdba fix(pack): tolerate imported governance validation)
- Removed stale generated-manifest validation drift. (84c459505c82 fix(generated): refresh stale artifact manifest)
- Resolved the generated-manifest drift warning. (79da4f6c876c chore(queue): reconcile completed review gates)
- stale queue blocker guidance no longer appears in Harness doctor or self-check. (6246811cf02e fix(recovery): clear remaining validation warnings)
- AIDE Lite validation no longer reports near-budget ledger entries as warnings. (6246811cf02e fix(recovery): clear remaining validation warnings)

## Docs

- documented Q27 commit, changelog, and WorkUnit recovery workflows. (0de5071ded87 docs(aide): document commit discipline and recovery workflows)
- documented Q28 Git workflow policy, branch roles, and promotion gates. (c305b581855a docs(git): document AIDE branch workflow policy)
- documented Q29 helper workflow, dry-run defaults, safety gates, fixture-only mutation tests, and Q30 next phase. (da209850bcd7 docs(git): document helper workflow and safety gates)
- record AIDE-specific dev/main branch workflow guidance. (19cb12a346f7 docs(git): document AIDE dev main workflow)
- recorded Q31 baseline validation evidence scaffold. (7a15b0ed97dd chore(pack): add Q31 governance export sync packet)
- Recorded Q31 portable governance export behavior and target sync boundaries. (62d13ad71795 docs(pack): document portable governance sync)
- recorded Q31 evidence and target-sync readiness. (ca2cc5a1b559 chore(pack): regenerate aide-lite-pack-v0)
- Documented preview-only release draft workflow and target-pack boundary. (453fe6aa9d66 docs(changelog): document release draft workflow)

## Tests

- deterministic Q27 coverage for commit lint, changelog preview, and WorkUnit no-op recovery. (f97d7736d0c0 test(aide): cover commit lint and WorkUnit recovery)
- covered deterministic changelog golden tasks and short-id task recovery fixtures. (600c5fb2e61b chore(pack): export commit and recovery policies)
- added Q28 branch role, workflow detection, and policy guard coverage. (eaaec3594b8b test(git): cover branch roles and workflow detection)
- added fixture Git coverage for Q29 helper land, promote, prune, dirty, unknown-role, protected-branch, and no-push behavior. (990d9cf0dbdc test(git): cover fixture land promote and prune)
- recorded fixture Git helper coverage and 20/20 golden task pass. (31bd0b29115c chore(pack): export Git helper policies)
- Q30 test coverage follows in the next commit. (7d4302cf01da feat(aide-lite): report AIDE dev main branch plan)
- added Q30 AIDE branch policy and branch-plan coverage. (8ae66d532800 test(git): cover AIDE branch policy validation)
- keep AIDE Lite selftest aligned with Q30 golden tasks. (778aaadd0afe test(git): include Q30 artifacts in selftest fixture)
- added Q30 export-boundary coverage. (0e62caef186f chore(pack): export updated Git workflow policy)
- added Q31 fixture import governance coverage. (b1d2e0f99281 test(pack): cover fixture import governance commands)
- updated safe import expectations for portable docs/reference governance docs. (b1d2e0f99281 test(pack): cover fixture import governance commands)
- Re-ran Q31 fixture import coverage and AIDE Lite selftest. (7119f14dbdba fix(pack): tolerate imported governance validation)
- exported Q31 golden tasks and fixture import coverage. (ca2cc5a1b559 chore(pack): regenerate aide-lite-pack-v0)
- Added Q34 changelog parser and preview output coverage. (160de9a7108a test(changelog): cover commit parsing and preview outputs)

## Internal

- recorded Q27 blocker state and evidence. (65689f6b0ca2 chore(aide): record Q27 prerequisite blocker)
- recorded Q28 blocker state and evidence. (1d9469676f16 chore(git): record Q28 prerequisite blocker)
- recorded Q29 blocker state and evidence. (8ac68636493c chore(git): record Q29 prerequisite blocker)
- reopened Q27 governance packet for implementation from the repaired baseline. (57b73ba81a94 chore(aide): add Q27 commit and recovery governance packet)
- optional local commit-msg hook template and commit template. (86974c90938c policy(aide): define structured commits and WorkUnit recovery)
- Q27 validation anchors and golden-task runners. (2146efa0db8f feat(aide-lite): add commit and task recovery commands)
- golden-task reports now include Q27 quality gates. (f97d7736d0c0 test(aide): cover commit lint and WorkUnit recovery)
- command catalog now lists Q27 AIDE Lite command families. (0de5071ded87 docs(aide): document commit discipline and recovery workflows)
- exported Q27 commit and recovery governance to the portable pack. (600c5fb2e61b chore(pack): export commit and recovery policies)
- reopened Q28 governance packet for implementation. (70056d8ac16a policy(git): add Q28 workflow governance packet)
- Q28 remains report-only and does not implement branch mutation. (5cb6dea4fb4c policy(git): define branch roles and promotion rules)
- Q28 validation now checks Git workflow policy anchors. (f4b8347da2be feat(aide-lite): add report-only Git workflow detection)
- added golden tasks for future no-call Git workflow policy checks. (eaaec3594b8b test(git): cover branch roles and workflow detection)
- exported Q28 Git workflow policies and helper tests in the portable AIDE Lite pack. (0fb6bb2872d7 chore(pack): export Git workflow policies)
- reopened Q29 governance packet for Git helper implementation. (58749c90cdc6 policy(git): add Q29 helper governance packet)
- exported Q29 Git helper governance and evidence artifacts. (31bd0b29115c chore(pack): export Git helper policies)
- added Q30 governance packet and baseline evidence. (71e3ad1231c2 policy(git): add Q30 AIDE dev main sync packet)
- recorded AIDE-specific branch policy and non-mutating dev/main plan. (cfefee11a38a policy(git): define AIDE dev main branch policy)
- added AIDE-specific dev/main branch plan reporting. (7d4302cf01da feat(aide-lite): report AIDE dev main branch plan)
- expanded deterministic golden task catalog. (8ae66d532800 test(git): cover AIDE branch policy validation)
- refresh profile and command catalog state truth for Q30. (19cb12a346f7 docs(git): document AIDE dev main workflow)
- refreshed Q30 export pack artifacts and evidence for review. (0e62caef186f chore(pack): export updated Git workflow policy)
- added Q31 governance export sync queue packet. (7a15b0ed97dd chore(pack): add Q31 governance export sync packet)
- added Q31 export/import policy anchors and golden tasks. (802052185200 policy(pack): include commit recovery and Git workflow files)
- refreshed the exported AIDE Lite Pack with portable governance outputs. (ca2cc5a1b559 chore(pack): regenerate aide-lite-pack-v0)
- Recorded baseline validation evidence before implementation changes. (2471b73deb67 policy(changelog): add Q34 release draft governance packet)
- Added no-call golden tasks for release notes previews, malformed commit reporting, and JSON shape. (160de9a7108a test(changelog): cover commit parsing and preview outputs)
- Exported portable changelog preview support through the AIDE Lite pack. (e0606831f7a9 chore(pack): export changelog preview support)
- Added a queue-scoped recovery packet for post-Q34 warning cleanup. (dc56ec6a76a4 chore(queue): add warning reconciliation packet)
- Recorded QFIX-03 warning inventory evidence. (84c459505c82 fix(generated): refresh stale artifact manifest)
- Removed stale queue review blockers from AIDE-local queue state. (79da4f6c876c chore(queue): reconcile completed review gates)
- QFIX-03 evidence and generated artifacts refreshed. (6246811cf02e fix(recovery): clear remaining validation warnings)

## Risks

- Q27 policy/tooling implementation is deferred until Q25 baseline repair. (65689f6b0ca2 chore(aide): record Q27 prerequisite blocker)
- Git workflow policy implementation is deferred until Q27 repair. (1d9469676f16 chore(git): record Q28 prerequisite blocker)
- merge/land/promote helper implementation is deferred until Q27 and Q28 repair. (8ac68636493c chore(git): record Q29 prerequisite blocker)
- documented that Q29 does not create dev, promote main, push, prune, or apply GitHub protection. (31bd0b29115c chore(pack): export Git helper policies)
- documented that Q30 is report-only and does not create or push dev. (71e3ad1231c2 policy(git): add Q30 AIDE dev main sync packet)
- documented future dev creation commands as not run by Q30. (cfefee11a38a policy(git): define AIDE dev main branch policy)
- Older commit history still contains malformed or legacy entries that require review before any future release promotion. (e0606831f7a9 chore(pack): export changelog preview support)
- Six early queue review-gate warnings remain pending review reconciliation. (84c459505c82 fix(generated): refresh stale artifact manifest)
- Reviews are accepted with notes and do not imply product readiness or release readiness. (79da4f6c876c chore(queue): reconcile completed review gates)

## Follow-up

- Q28 Git Workflow Policy v0 can now be redone from Q27 commit/recovery discipline. (600c5fb2e61b chore(pack): export commit and recovery policies)
- define branch roles, workflow policies, report-only detection, tests, docs, and export pack integration. (70056d8ac16a policy(git): add Q28 workflow governance packet)
- Q35 should address GitHub protection and CI advisory policy without publishing releases. (e0606831f7a9 chore(pack): export changelog preview support)
- Refresh generated artifacts, reconcile eligible review gates, and rerun validation. (dc56ec6a76a4 chore(queue): add warning reconciliation packet)
- Complete QFIX-03 final validation and evidence. (79da4f6c876c chore(queue): reconcile completed review gates)

## Malformed Commits

- a1e6ed6ecf36 chore: add q25 importer scope repair packet: missing_required_headings: ## Summary, ## Why, ## Changed, ## Validation, ## Changelog, ## Risks, ## Follow-up; missing_changelog_category
- 1b44aa256fe9 fix: repair aide lite pack integrity checks: missing_required_headings: ## Summary, ## Why, ## Changed, ## Validation, ## Changelog, ## Risks, ## Follow-up; missing_changelog_category; legacy_semi_structured_body
- 7313501a83d2 fix: narrow cross-repo import scope: missing_required_headings: ## Summary, ## Why, ## Changed, ## Validation, ## Changelog, ## Risks, ## Follow-up; missing_changelog_category; legacy_semi_structured_body
- 2609ba6bea47 chore: refresh post-adapter state truth: missing_required_headings: ## Summary, ## Why, ## Changed, ## Validation, ## Changelog, ## Risks, ## Follow-up; missing_changelog_category; legacy_semi_structured_body
- fe2ba90ebe63 docs: record q25 repair evidence: missing_required_headings: ## Summary, ## Why, ## Changed, ## Validation, ## Changelog, ## Risks, ## Follow-up; missing_changelog_category; legacy_semi_structured_body
- e098f80c97e3 fix: complete q25 pack integrity revalidation: missing_required_headings: ## Summary, ## Why, ## Changed, ## Validation, ## Changelog, ## Risks, ## Follow-up; missing_changelog_category; legacy_semi_structured_body
- 5b7ae1a1a136 chore: record q26 eureka handover checkpoint: missing_required_headings: ## Summary, ## Why, ## Changed, ## Validation, ## Changelog, ## Risks, ## Follow-up; missing_changelog_category; legacy_semi_structured_body
- 05330b0842a3 fix: harden q25 pack provenance validation: missing_required_headings: ## Summary, ## Why, ## Changed, ## Validation, ## Changelog, ## Risks, ## Follow-up; missing_changelog_category; legacy_semi_structured_body

## Release Caveat

- Preview only. No tags, GitHub Releases, branch mutation, or publishing were performed.
