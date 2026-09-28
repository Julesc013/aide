# AIDE Release Notes Preview

This is a deterministic preview only. It does not publish a release.

source_range: HEAD latest 50 commits
source_head: 4b5854f2f9dbeea7cf246946caf02d829a16c757
preview_only: true

## Highlights

- Added: explicit bounded maintainer job inspect/run/recover commands. (5ea1f7cdd53c)
- Changed: Task OS golden validation leaves source projections unchanged. (e185d2898fb2)
- Fixed: installed Lite Task OS reports no selected task for an empty queue. (f00d937e2368)
- Fixed: project-owned Lite target queues no longer receive AIDE source-phase next-work advice. (e88a1468acd2)
- Fixed: target Task OS routing follows its declared profile even when a queue ID matches an AIDE source task. (b9d2b150c39c)
- Fixed: target next-work explanation remains accurate even when queue IDs collide with source IDs. (52e1f194ebd2)
- Fixed: local draft lifecycle claims now match the bounded Windows apply candidates. (bc1867a06933)
- Fixed: preview effect evidence now identifies its exact commit range and replay state. (6e8af2bd8d16)
- Fixed: allow explicit Windows recovery of an exact partial portable import without replaying changed project bytes. (547ea2b09235)
- Fixed: refuse forged partial import ownership and stale controls during recovery. (052a0a926527)
- Fixed: prevent controls and resolution drift during final partial-import publication. (dfc8048bc005)
- Fixed: default Git query report churn and lost cleanup after interruption. (5ea1f7cdd53c)
- Fixed: Source maintainer test and evaluation entrypoints enforce bounded job admission. (11226a6e7fd0)
- Fixed: Generator source output allocation requires capacity reservations. (8acfecc44e61)
- Fixed: Recovery cannot bypass source-output resource qualification. (b325deeaca74)
- Fixed: Task status inspection no longer generates tracked reports by default. (0302b18c724d)
- Fixed: Candidate stable interface includes requested customization and recovery forms. (f0eabe41265d)
- Fixed: Explicit import feedback refuses every supplied input pack and the target. (c6d104f665e3)
- Removed: Two verified duplicate consumer ZIP expansions. (119529d076fd)
- Docs: preserve focused source review with explicit qualification limits. (36e1a6d54aa0)
- Docs: retain resource source review and bounded product validation routing. (8aa60c7bb8a2)
- Docs: Preserve accepted resource and product validation checkpoint. (260139d2d108)
- Docs: Align current source status and already adopted specification boundaries. (71ef35127845)
- Tests: avoid full design-family fixture installs for focused partial-recovery boundaries. (e87386e55eda)

## Validation Summary

- b3a001befaac: PASS: Local, origin, ls-remote and GitHub API all observed dev at 2defcad5 after fast-forward and normal push.
- 5561aecdb608: PASS: Fresh extracted-ZIP safe import applied 816 owned files; installed context, pack and verify exited zero with zero verifier errors.
- b45010280e5e: PASS: 31 command log hashes and exit codes matched the pinned canary summary.
- 736e3f9ac027: PASS: git plan returned ready_dry_run before branch creation.
- a7254d7d4c9c: PASS: task inspect reports complete with zero missing evidence.
- d292253b0994: PASS: exact candidate checks and four-commit range passed before effect.
- f00d937e2368: PASS: the new regression failed on unmodified source with incidental X-OS-01 identity.
- 04caefe65986: PASS: external review report hash matched and source worktree stayed clean before this evidence edit.
- e88a1468acd2: PASS: one-item target regression failed on old source with X-OS-01 and passed after repair.
- b9d2b150c39c: PASS: copied-ID target regression failed before the role repair and passes afterward.

## Known Risks

- b3a001befaac: Synthetic update fixtures and local previews do not establish a shipping support profile or public stable release.
- 5561aecdb608: Local preview and synthetic packs cannot establish stable release or published-predecessor support.
- b45010280e5e: This is preview-only evidence; the synthetic rollback successor and in-process interruption do not establish published or hostile-process guarantees.
- 736e3f9ac027: The Task OS report-truth finding and final released-byte qualifications remain unresolved.
- a7254d7d4c9c: The evaluation acceptance does not itself authorize dev mutation; the Task OS source defect and stable release gates remain open.
- d292253b0994: Empty-target Task OS report truth remains defective; synthetic rollback and local preview checks do not qualify a stable release.
- f00d937e2368: Source tests do not qualify the unchanged preview archives or the eventual published release.
- 04caefe65986: The reviewed source commit is f00d937e; this later evidence-only commit is not a changed-source review substitute.
- e88a1468acd2: Old export and release preview bytes do not contain this source repair; canonical provenance is red until regenerated.
- b9d2b150c39c: Legacy profile-absent queues retain exact ID fallback; this is not a universal ownership classifier.

## Follow-up

- b3a001befaac: Qualify final declared Windows lifecycle, restart, offline and context/evidence journeys from frozen bytes, then proceed through separate exact release gates.
- 5561aecdb608: Finish and independently review lifecycle/restart consumers; implement any real defect in a separate scoped source task.
- b45010280e5e: Admit a bounded Task OS source repair, regenerate reviewed assets, and recheck installed consumers before final release acceptance.
- 736e3f9ac027: Freeze the exact integration candidate, run canonical checks, seek independent effect review, then act only on matching refs.
- a7254d7d4c9c: Run exact candidate checks, freeze an external effect manifest and obtain independent review before a fresh dev preflight.
- d292253b0994: Independently review and integrate this closeout, then implement and test the bounded Task OS source repair.
- f00d937e2368: Obtain independent exact source review, then project through the current generator and rerun the installed consumer before a dev effect.
- 04caefe65986: Admit and implement the target-owned nonempty queue routing repair, review its delta, then regenerate delivered artifacts once.
- e88a1468acd2: Obtain independent exact source delta review, then regenerate once through the current generator and qualify installed target queues.
- b9d2b150c39c: Independently review this exact changed source, then regenerate once and qualify zero- and one-item installed targets.

## Warnings

- None.

## Preview Caveat

- This draft is not an official release note and does not create tags or GitHub Releases.
