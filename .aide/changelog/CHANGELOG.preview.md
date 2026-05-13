# AIDE Changelog Preview

source_range: HEAD~20..HEAD
commit_count: 20
release_publishing: false

## Added

- canonical Git workflow policy files for branch roles, promotion gates, sync posture, prune posture, and project profiles. (5cb6dea4fb4c policy(git): define branch roles and promotion rules)
- report-only Git workflow detection and branch-role command surface. (f4b8347da2be feat(aide-lite): add report-only Git workflow detection)
- dry-run Git helper command surface for local branch planning, landing, promotion, sync, and prune guards. (8fc3bfe63dcd feat(git): add dry-run branch helper commands)

## Changed

- WorkUnit recovery preflight now includes branch-role inspection. (5cb6dea4fb4c policy(git): define branch roles and promotion rules)
- updated next-phase guidance from Q28 redo to Q29 merge/land/promote helpers. (c305b581855a docs(git): document AIDE branch workflow policy)
- Q28 queue state now stops at needs_review with complete evidence. (0fb6bb2872d7 chore(pack): export Git workflow policies)

## Fixed

- made task inspection resolve compact short task ids through the queue index. (600c5fb2e61b chore(pack): export commit and recovery policies)
- AIDE Lite selftest fixture now includes Q28 policy files when Q28 golden tasks run. (0fb6bb2872d7 chore(pack): export Git workflow policies)

## Docs

- documented Q27 commit, changelog, and WorkUnit recovery workflows. (0de5071ded87 docs(aide): document commit discipline and recovery workflows)
- documented Q28 Git workflow policy, branch roles, and promotion gates. (c305b581855a docs(git): document AIDE branch workflow policy)
- documented Q29 helper workflow, dry-run defaults, safety gates, fixture-only mutation tests, and Q30 next phase. (da209850bcd7 docs(git): document helper workflow and safety gates)
- record AIDE-specific dev/main branch workflow guidance. (19cb12a346f7 docs(git): document AIDE dev main workflow)

## Tests

- deterministic Q27 coverage for commit lint, changelog preview, and WorkUnit no-op recovery. (f97d7736d0c0 test(aide): cover commit lint and WorkUnit recovery)
- covered deterministic changelog golden tasks and short-id task recovery fixtures. (600c5fb2e61b chore(pack): export commit and recovery policies)
- added Q28 branch role, workflow detection, and policy guard coverage. (eaaec3594b8b test(git): cover branch roles and workflow detection)
- added fixture Git coverage for Q29 helper land, promote, prune, dirty, unknown-role, protected-branch, and no-push behavior. (990d9cf0dbdc test(git): cover fixture land promote and prune)
- recorded fixture Git helper coverage and 20/20 golden task pass. (31bd0b29115c chore(pack): export Git helper policies)
- Q30 test coverage follows in the next commit. (7d4302cf01da feat(aide-lite): report AIDE dev main branch plan)
- added Q30 AIDE branch policy and branch-plan coverage. (8ae66d532800 test(git): cover AIDE branch policy validation)
- keep AIDE Lite selftest aligned with Q30 golden tasks. (778aaadd0afe test(git): include Q30 artifacts in selftest fixture)

## Internal

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

## Risks

- documented that Q29 does not create dev, promote main, push, prune, or apply GitHub protection. (31bd0b29115c chore(pack): export Git helper policies)
- documented that Q30 is report-only and does not create or push dev. (71e3ad1231c2 policy(git): add Q30 AIDE dev main sync packet)
- documented future dev creation commands as not run by Q30. (cfefee11a38a policy(git): define AIDE dev main branch policy)

## Follow-up

- Q28 Git Workflow Policy v0 can now be redone from Q27 commit/recovery discipline. (600c5fb2e61b chore(pack): export commit and recovery policies)
- define branch roles, workflow policies, report-only detection, tests, docs, and export pack integration. (70056d8ac16a policy(git): add Q28 workflow governance packet)

## Malformed Commits

- None.
