# AIDE Changelog Preview

This file is generated from local Git history and is a preview only.

source_range: HEAD latest 50 commits
source_head: 84e4a7330ce93e116c8c6af0b181d8756af6f647
commit_count: 50
malformed_count: 0
preview_only: true
release_publishing: false

## Summary

- Added: 1
- Changed: 1
- Fixed: 16
- Removed: 1
- Docs: 4
- Tests: 1
- Internal: 27

## Added

- explicit bounded maintainer job inspect/run/recover commands. (5ea1f7cdd53c feat(execution): bound maintainer jobs and retire owned scratch)

## Changed

- Task OS golden validation leaves source projections unchanged. (e185d2898fb2 test(task-os): isolate golden report writes in admitted scratch)

## Fixed

- installed Lite Task OS reports no selected task for an empty queue. (f00d937e2368 fix(task-os): keep empty target queue reports truthful)
- project-owned Lite target queues no longer receive AIDE source-phase next-work advice. (e88a1468acd2 fix(task-os): keep target queue next work project-owned)
- target Task OS routing follows its declared profile even when a queue ID matches an AIDE source task. (b9d2b150c39c fix(task-os): route target next work by declared profile)
- target next-work explanation remains accurate even when queue IDs collide with source IDs. (52e1f194ebd2 fix(task-os): keep copied-id target reason truthful)
- local draft lifecycle claims now match the bounded Windows apply candidates. (bc1867a06933 fix(release): distinguish lifecycle planners from bounded apply)
- preview effect evidence now identifies its exact commit range and replay state. (6e8af2bd8d16 fix(release): bind exact preview effect evidence)
- allow explicit Windows recovery of an exact partial portable import without replaying changed project bytes. (547ea2b09235 feat(import): recover exact partial Windows portable imports)
- refuse forged partial import ownership and stale controls during recovery. (052a0a926527 fix(import): reject forged partial recovery intents)
- prevent controls and resolution drift during final partial-import publication. (dfc8048bc005 fix(import): pin recovery inputs through intent retirement)
- default Git query report churn and lost cleanup after interruption. (5ea1f7cdd53c feat(execution): bound maintainer jobs and retire owned scratch)
- Source maintainer test and evaluation entrypoints enforce bounded job admission. (11226a6e7fd0 fix(execution): enforce resource admission on maintainer commands)
- Generator source output allocation requires capacity reservations. (8acfecc44e61 fix(execution): reserve canonical generator output capacity)
- Recovery cannot bypass source-output resource qualification. (b325deeaca74 fix(execution): qualify canonical outputs during crash recovery)
- Task status inspection no longer generates tracked reports by default. (0302b18c724d fix(queue): inspect task status without rewriting reports)
- Candidate stable interface includes requested customization and recovery forms. (f0eabe41265d fix(contract): retain customization and partial recovery interfaces)
- Explicit import feedback refuses every supplied input pack and the target. (c6d104f665e3 fix(import): protect predecessor packs from feedback output)

## Removed

- Two verified duplicate consumer ZIP expansions. (119529d076fd chore(resource): retire verified duplicate consumer expansions)

## Docs

- preserve focused source review with explicit qualification limits. (36e1a6d54aa0 docs(recovery): preserve exact input-guard review)
- retain resource source review and bounded product validation routing. (8aa60c7bb8a2 docs(execution): preserve accepted resource source and bounded routing)
- Preserve accepted resource and product validation checkpoint. (260139d2d108 docs(evidence): preserve accepted bounded execution checkpoint)
- Align current source status and already adopted specification boundaries. (71ef35127845 docs(policy): align runtime status and adopted specification roles)

## Tests

- avoid full design-family fixture installs for focused partial-recovery boundaries. (e87386e55eda test(import): bound fixtures for partial recovery regressions)

## Internal

- Converge local preview release metadata without rebuilding archives. (2defcad541d0 chore(release): converge Lite contract preview metadata)
- Close the bounded stable contract source and local-preview dev integration records. (b3a001befaac chore(queue): close stable Lite contract dev integration)
- Route mandatory delivered Lite consumer checks through a bounded WorkUnit. (5561aecdb608 chore(queue): admit delivered Lite consumer prequalification)
- preserve bounded local consumer evidence and a reproducible Task OS repair trigger. (b45010280e5e test(lite): record delivered consumer prequalification)
- create a bounded route for evidence-only dev integration. (736e3f9ac027 chore(queue): admit Lite evidence dev integration)
- complete a separate evidence-only dev integration review packet. (a7254d7d4c9c chore(queue): freeze Lite evidence integration packet)
- preserve verified Windows Lite preview evidence integration and unresolved release gates. (d292253b0994 chore(lite): close observed consumer evidence dev effect)
- preserve independent Task OS source review and its release-blocking follow-up. (04caefe65986 chore(task-os): record exact empty-queue source review)
- preserve the exact Task OS repaired-source review result. (75406123ccb0 chore(task-os): preserve accepted target routing review)
- preserve exact Q48 source review and remaining gates. (59286688dfce chore(release): preserve accepted draft source review)
- admit current Lite preview projection and qualification task. (0509e1611b18 chore(release): admit current Lite artifact projection)
- refresh local Lite preview assets and bind current source evidence. (dc8697e336eb chore(release): project accepted Lite source into preview assets)
- converge source-ancestor release metadata without rebuilding assets. (10fd7a207f16 chore(release): converge committed Lite preview metadata)
- preserve committed Lite preview qualification evidence. (22257dc6ad9e chore(release): preserve committed Lite preview qualification)
- preserve reviewed Lite dev integration and current release gaps. (493e3f13c1b2 chore(release): record reviewed Lite dev integration)
- route Windows process-restart qualification through a bounded task. (5f2441d18772 chore(release): admit forced restart qualification)
- record local forced-restart qualification and precise remaining recovery obligation. (f44f3a28fc08 chore(release): record delivered Lite forced restart evidence)
- repair local forced-restart evidence wording before dev integration. (e88b1c2ee6f3 chore(release): correct forced restart evidence closeout truth)
- route partial import recovery through a bounded reviewed source task. (d4b7657d9c0e chore(release): admit partial import recovery source work)
- Preserve reviewed feedback repair and the resource-bound continuation. (53be4fc43ab2 chore(queue): preserve feedback repair review and resource checkpoint)
- Consolidate dev source and preserve the stopped release/rollout checkpoint. (a1fe9fd57ac1 chore(git): consolidate dev and record release rollout checkpoint)
- Preserve scoped documentation acceptance and the next qualified dev effect. (1d70597894e3 chore(queue): preserve documentation acceptance and dev effect)
- Activate bounded execution under the approved Temporary parent. (e18f983b0937 chore(execution): activate owner-selected bounded qualification storage)
- Make live scratch observation resilient to transient fixture deletion. (8040b10a5d2c fix(execution): tolerate transient scratch scan disappearance)
- Preserve current-source qualification and remaining delivery gates. (a835cbad6d5b docs(execution): record reviewed runner and importer qualification)
- Advance partial-import recovery from source validation to artifact qualification. (1d3d9fe1bb51 docs(import): record complete source suite and artifact gate)
- Route current-source Lite artifact qualification through a bounded WorkUnit. (84e4a7330ce9 chore(release): admit current Lite artifact projection)

## Malformed Commits

- None.

## Release Caveat

- Preview only. No tags, GitHub Releases, branch mutation, or publishing were performed.
