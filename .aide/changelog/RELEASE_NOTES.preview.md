# AIDE Release Notes Preview

This is a deterministic preview only. It does not publish a release.

source_range: HEAD latest 50 commits
source_head: 4c32a8edd8aa8ea129609c6aedb534e6dfcf16f1
preview_only: true

## Highlights

- Added: explicit bounded maintainer job inspect/run/recover commands. (5ea1f7cdd53c)
- Added: Separate first-stable Lite candidate archive generation and validation. (24bd7d0d88c6)
- Changed: Task OS golden validation leaves source projections unchanged. (e185d2898fb2)
- Changed: Record exact source-review acceptance for the unpublished stable builder. (a6725d83db10)
- Changed: Refresh portable AIDE Lite pack from accepted dev source. (4c32a8edd8aa)
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
- Fixed: Reject unsafe Windows archive paths in the unpublished stable builder. (34c87052f7e3)
- Fixed: Bound tar metadata parsing in the unpublished stable release validator. (59db02a0e6c3)
- Removed: Two verified duplicate consumer ZIP expansions. (119529d076fd)
- Docs: preserve focused source review with explicit qualification limits. (36e1a6d54aa0)
- Docs: retain resource source review and bounded product validation routing. (8aa60c7bb8a2)
- Docs: Preserve accepted resource and product validation checkpoint. (260139d2d108)
- Docs: Align current source status and already adopted specification boundaries. (71ef35127845)
- Tests: avoid full design-family fixture installs for focused partial-recovery boundaries. (e87386e55eda)

## Validation Summary

- 22257dc6ad9e: PASS: four release replay commands changed zero paths; archive hashes unchanged.
- 6e8af2bd8d16: PASS: exact 22257dc6 12-commit check, task inspect with eight evidence files and no missing evidence, git diff --check.
- 493e3f13c1b2: PASS: exact effect candidate 6e8af2bd had a 13-commit range pass and clean four-command release replay.
- 5f2441d18772: PASS: canonical repository validate.
- f44f3a28fc08: PASS: canonical validate, task inspect with four evidence files and zero missing, explicit staged whitespace check.
- e88b1c2ee6f3: PASS: canonical validate, task inspect with five evidence files and zero missing, explicit staged whitespace check.
- d4b7657d9c0e: PASS: canonical validate; prior task inspect complete with six evidence files and zero missing.
- 547ea2b09235: PASS: Python compile and staged whitespace check.
- 052a0a926527: PASS: six focused Windows recovery regressions, Python compile and staged whitespace check.
- dfc8048bc005: PASS: fresh/update recovery test and three guard/resolution tests, including second-process denial and exit-77 cleanup.

## Known Risks

- 22257dc6ad9e: This evidence-only commit is distinct from source 0509e161, projection dc8697e3 and metadata 10fd7a20.
- 6e8af2bd8d16: This commit changes the effect subject and therefore needs its own exact policy-range receipt and review.
- 493e3f13c1b2: This evidence-only closeout is distinct from the reviewed source/artifact effect commit and requires its own qualified dev effect.
- 5f2441d18772: Current archive is a local preview, and a synthetic successor is not a published predecessor.
- f44f3a28fc08: Synthetic rollback successor and local preview bytes are not published release qualification.
- e88b1c2ee6f3: The earlier f44f3a28 effect review remains NO GO; this new commit needs focused review.
- d4b7657d9c0e: The local ZIP remains a preview and cannot qualify source changes made later.
- 547ea2b09235: Older intents remain safe refusal; this source candidate has not qualified delivered archives or final release.
- 052a0a926527: This remains a source candidate; delivered archives, dev integration and stable release are unqualified.
- dfc8048bc005: This is a Windows source candidate, not qualified delivered bytes or an integrated release.

## Follow-up

- 22257dc6ad9e: Freeze this exact candidate, replay once, obtain independent artifact/effect verdict, then perform only qualified dev effect.
- 6e8af2bd8d16: Run the final exact range and clean replay, then request focused independent rereview before dev integration.
- 493e3f13c1b2: Independently review this exact closeout, integrate if qualified, then execute final Lite profile qualification.
- 5f2441d18772: Run abrupt-exit consumers, preserve byte-bound evidence, seek independent technical review and integrate truthful closeout.
- f44f3a28fc08: Independently review this exact evidence candidate for a dev effect, then implement and qualify bounded partial recovery.
- e88b1c2ee6f3: Obtain exact focused review; if accepted, perform one-writer dev fast-forward and normal push after fresh checks, then route partial recovery source work.
- d4b7657d9c0e: Add red adversarial regressions, implement explicit recovery, obtain independent source review, then project and qualify new delivered bytes.
- 547ea2b09235: Finish importer suite, obtain independent source review, then project and qualify new delivered bytes before dev integration.
- 052a0a926527: Finish combined tests, obtain independent exact rereview, then project and qualify new delivered bytes.
- dfc8048bc005: Obtain exact source rereview, run the final importer suite, then project and qualify the delivered archive.

## Warnings

- None.

## Preview Caveat

- This draft is not an official release note and does not create tags or GitHub Releases.
