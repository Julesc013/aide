# AIDE Changelog Preview

source_range: HEAD~20..HEAD
commit_count: 20
release_publishing: false

## Added

- canonical AIDE commit discipline and WorkUnit recovery policy. (86974c90938c policy(aide): define structured commits and WorkUnit recovery)
- AIDE Lite commit, changelog, and task recovery command surfaces. (2146efa0db8f feat(aide-lite): add commit and task recovery commands)
- canonical Git workflow policy files for branch roles, promotion gates, sync posture, prune posture, and project profiles. (5cb6dea4fb4c policy(git): define branch roles and promotion rules)
- report-only Git workflow detection and branch-role command surface. (f4b8347da2be feat(aide-lite): add report-only Git workflow detection)

## Changed

- WorkUnit recovery preflight now includes branch-role inspection. (5cb6dea4fb4c policy(git): define branch roles and promotion rules)
- updated next-phase guidance from Q28 redo to Q29 merge/land/promote helpers. (c305b581855a docs(git): document AIDE branch workflow policy)

## Fixed

- made task inspection resolve compact short task ids through the queue index. (600c5fb2e61b chore(pack): export commit and recovery policies)

## Docs

- documented Q27 commit, changelog, and WorkUnit recovery workflows. (0de5071ded87 docs(aide): document commit discipline and recovery workflows)
- documented Q28 Git workflow policy, branch roles, and promotion gates. (c305b581855a docs(git): document AIDE branch workflow policy)

## Tests

- deterministic Q27 coverage for commit lint, changelog preview, and WorkUnit no-op recovery. (f97d7736d0c0 test(aide): cover commit lint and WorkUnit recovery)
- covered deterministic changelog golden tasks and short-id task recovery fixtures. (600c5fb2e61b chore(pack): export commit and recovery policies)
- added Q28 branch role, workflow detection, and policy guard coverage. (eaaec3594b8b test(git): cover branch roles and workflow detection)

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

## Risks

- Q27 policy/tooling implementation is deferred until Q25 baseline repair. (65689f6b0ca2 chore(aide): record Q27 prerequisite blocker)
- Git workflow policy implementation is deferred until Q27 repair. (1d9469676f16 chore(git): record Q28 prerequisite blocker)
- merge/land/promote helper implementation is deferred until Q27 and Q28 repair. (8ac68636493c chore(git): record Q29 prerequisite blocker)

## Follow-up

- Q28 Git Workflow Policy v0 can now be redone from Q27 commit/recovery discipline. (600c5fb2e61b chore(pack): export commit and recovery policies)
- define branch roles, workflow policies, report-only detection, tests, docs, and export pack integration. (70056d8ac16a policy(git): add Q28 workflow governance packet)

## Malformed Commits

- 7313501a83d2 fix: narrow cross-repo import scope: commit subject follows type(scope): summary; commit type cannot be validated without subject match; commit body contains heading: ## Summary; commit body heading has content: ## Summary; commit body heading has bullet content: ## Summary; commit body contains heading: ## Why; commit body heading has content: ## Why; commit body heading has bullet content: ## Why; commit body contains heading: ## Changed; commit body heading has content: ## Changed; commit body heading has bullet content: ## Chan
- 2609ba6bea47 chore: refresh post-adapter state truth: commit subject follows type(scope): summary; commit type cannot be validated without subject match; commit body contains heading: ## Summary; commit body heading has content: ## Summary; commit body heading has bullet content: ## Summary; commit body contains heading: ## Why; commit body heading has content: ## Why; commit body heading has bullet content: ## Why; commit body contains heading: ## Changed; commit body heading has content: ## Changed; commit body heading has bullet content: ## Chan
- fe2ba90ebe63 docs: record q25 repair evidence: commit subject follows type(scope): summary; commit type cannot be validated without subject match; commit body contains heading: ## Summary; commit body heading has content: ## Summary; commit body heading has bullet content: ## Summary; commit body contains heading: ## Why; commit body heading has content: ## Why; commit body heading has bullet content: ## Why; commit body contains heading: ## Changed; commit body heading has content: ## Changed; commit body heading has bullet content: ## Chan
- e098f80c97e3 fix: complete q25 pack integrity revalidation: commit subject follows type(scope): summary; commit type cannot be validated without subject match; commit body contains heading: ## Summary; commit body heading has content: ## Summary; commit body heading has bullet content: ## Summary; commit body contains heading: ## Why; commit body heading has content: ## Why; commit body heading has bullet content: ## Why; commit body contains heading: ## Changed; commit body heading has content: ## Changed; commit body heading has bullet content: ## Chan
- 5b7ae1a1a136 chore: record q26 eureka handover checkpoint: commit subject follows type(scope): summary; commit type cannot be validated without subject match; commit body contains heading: ## Summary; commit body heading has content: ## Summary; commit body heading has bullet content: ## Summary; commit body contains heading: ## Why; commit body heading has content: ## Why; commit body heading has bullet content: ## Why; commit body contains heading: ## Changed; commit body heading has content: ## Changed; commit body heading has bullet content: ## Chan
- 05330b0842a3 fix: harden q25 pack provenance validation: commit subject follows type(scope): summary; commit type cannot be validated without subject match; commit body contains heading: ## Summary; commit body heading has content: ## Summary; commit body heading has bullet content: ## Summary; commit body contains heading: ## Why; commit body heading has content: ## Why; commit body heading has bullet content: ## Why; commit body contains heading: ## Changed; commit body heading has content: ## Changed; commit body heading has bullet content: ## Chan
