# AIDE Changelog Preview

This file is generated from local Git history and is a preview only.

source_range: HEAD latest 50 commits
source_head: 4c32a8edd8aa8ea129609c6aedb534e6dfcf16f1
commit_count: 50
malformed_count: 0
preview_only: true
release_publishing: false

## Summary

- Added: 2
- Changed: 3
- Fixed: 13
- Removed: 1
- Docs: 4
- Tests: 1
- Internal: 27

## Added

- explicit bounded maintainer job inspect/run/recover commands. (5ea1f7cdd53c feat(execution): bound maintainer jobs and retire owned scratch)
- Separate first-stable Lite candidate archive generation and validation. (24bd7d0d88c6 feat(release): build distinct first-stable Lite candidate assets)

## Changed

- Task OS golden validation leaves source projections unchanged. (e185d2898fb2 test(task-os): isolate golden report writes in admitted scratch)
- Record exact source-review acceptance for the unpublished stable builder. (a6725d83db10 docs(release): record accepted exact stable-builder source review)
- Refresh portable AIDE Lite pack from accepted dev source. (4c32a8edd8aa chore(release): refresh portable pack from accepted dev source)

## Fixed

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
- Reject unsafe Windows archive paths in the unpublished stable builder. (34c87052f7e3 fix(release): reject unsafe Windows archive members before extraction)
- Bound tar metadata parsing in the unpublished stable release validator. (59db02a0e6c3 fix(release): bound tar PAX metadata before archive parsing)

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
- Refresh local no-publish Lite preview artifacts from current source. (4b5854f2f9db chore(release): regenerate current Lite preview assets)
- Converge local preview provenance after the artifact commit. (dcb008e62b46 chore(release): converge post-commit preview metadata)
- Converge local Lite preview release provenance after commit. (49c7a04a1377 chore(release): converge committed Lite preview metadata)
- Record local preview qualification without changing product bytes. (e7c1760e8e5b docs(release): record delivered Lite preview qualification)
- Record local Lite preview integration and remaining release gates. (33abef7fca15 docs(release): record reviewed Lite preview dev effect)
- Track remaining Lite qualification separately from passed preview integration. (b74923195d0b chore(release): admit remaining Lite qualification)
- make managed scratch retirement work with ordinary readonly Git objects on Windows. (cf0c4434f260 fix(execution): retire readonly owned Git scratch after custody)
- Preserve bounded runner review for the dev integration gate. (b7f595424f04 chore(execution): record independent runner repair acceptance)
- Preserve delivered public CLI qualification checkpoint. (c6de695fbbd8 chore(release): record dev repair integration and public CLI canary)
- Record partitioned importer source qualification. (b94d7ba940e2 chore(release): bind integrated importer qualification)
- Bind installed task inspection qualification. (0259f81d8fca chore(release): qualify installed task inspection forms)
- Preserve exact local preview acceptance and remaining release obligations. (4dcd896b4a9b chore(release): bind exact Lite preview command coverage)
- Separate accepted local preview from public release effect. (f3f59303e5d0 chore(release): close exact Lite preview and admit stable effect)

## Malformed Commits

- None.

## Release Caveat

- Preview only. No tags, GitHub Releases, branch mutation, or publishing were performed.
