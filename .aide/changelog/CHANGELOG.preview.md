# AIDE Changelog Preview

source_range: HEAD~20..HEAD
commit_count: 20
release_publishing: false

## Added

- dry-run Git helper command surface for local branch planning, landing, promotion, sync, and prune guards. (8fc3bfe63dcd feat(git): add dry-run branch helper commands)

## Changed

- updated next-phase guidance from Q28 redo to Q29 merge/land/promote helpers. (c305b581855a docs(git): document AIDE branch workflow policy)
- Q28 queue state now stops at needs_review with complete evidence. (0fb6bb2872d7 chore(pack): export Git workflow policies)
- safe import now treats portable docs/reference governance docs as target-safe. (802052185200 policy(pack): include commit recovery and Git workflow files)
- Updated agent guidance for target sync and adapter-generated guidance inputs. (62d13ad71795 docs(pack): document portable governance sync)

## Fixed

- AIDE Lite selftest fixture now includes Q28 policy files when Q28 golden tasks run. (0fb6bb2872d7 chore(pack): export Git workflow policies)
- excluded AIDE-local Q30 branch-policy artifacts from portable pack truth. (0e62caef186f chore(pack): export updated Git workflow policy)
- imported target Git policy no longer fails solely because target-local helper plans have not been generated yet. (802052185200 policy(pack): include commit recovery and Git workflow files)
- Q31 governance validation no longer rejects target-style repos that do not contain a source export pack. (7119f14dbdba fix(pack): tolerate imported governance validation)

## Docs

- documented Q28 Git workflow policy, branch roles, and promotion gates. (c305b581855a docs(git): document AIDE branch workflow policy)
- documented Q29 helper workflow, dry-run defaults, safety gates, fixture-only mutation tests, and Q30 next phase. (da209850bcd7 docs(git): document helper workflow and safety gates)
- record AIDE-specific dev/main branch workflow guidance. (19cb12a346f7 docs(git): document AIDE dev main workflow)
- recorded Q31 baseline validation evidence scaffold. (7a15b0ed97dd chore(pack): add Q31 governance export sync packet)
- Recorded Q31 portable governance export behavior and target sync boundaries. (62d13ad71795 docs(pack): document portable governance sync)

## Tests

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

## Internal

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

## Risks

- documented that Q29 does not create dev, promote main, push, prune, or apply GitHub protection. (31bd0b29115c chore(pack): export Git helper policies)
- documented that Q30 is report-only and does not create or push dev. (71e3ad1231c2 policy(git): add Q30 AIDE dev main sync packet)
- documented future dev creation commands as not run by Q30. (cfefee11a38a policy(git): define AIDE dev main branch policy)

## Malformed Commits

- None.
