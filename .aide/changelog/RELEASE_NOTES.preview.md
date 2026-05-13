# AIDE Release Notes Preview

This is a deterministic preview only. It does not publish a release.

source_range: HEAD latest 50 commits
source_head: 6246811cf02ece09bd25b53ce0625919db658f51
preview_only: true

## Highlights

- Added: canonical AIDE commit discipline and WorkUnit recovery policy. (86974c90938c)
- Added: AIDE Lite commit, changelog, and task recovery command surfaces. (2146efa0db8f)
- Added: canonical Git workflow policy files for branch roles, promotion gates, sync posture, prune posture, and project profiles. (5cb6dea4fb4c)
- Added: report-only Git workflow detection and branch-role command surface. (f4b8347da2be)
- Added: dry-run Git helper command surface for local branch planning, landing, promotion, sync, and prune guards. (8fc3bfe63dcd)
- Added: Q34 release draft governance queue packet for preview-only changelog and release-note generation. (2471b73deb67)
- Added: preview-only changelog and release-note generator command surface. (52afde5b0161)
- Added: changelog policy, config, templates, release-notes JSON, and latest report support. (52afde5b0161)
- Added: Generated preview-only changelog and release-note draft artifacts for Q34 review. (e0606831f7a9)
- Changed: WorkUnit recovery preflight now includes branch-role inspection. (5cb6dea4fb4c)
- Changed: updated next-phase guidance from Q28 redo to Q29 merge/land/promote helpers. (c305b581855a)
- Changed: Q28 queue state now stops at needs_review with complete evidence. (0fb6bb2872d7)
- Changed: safe import now treats portable docs/reference governance docs as target-safe. (802052185200)
- Changed: Updated agent guidance for target sync and adapter-generated guidance inputs. (62d13ad71795)
- Changed: export/import policy now names portable changelog policy and templates. (52afde5b0161)
- Changed: Command catalog now lists changelog preview/validate/status. (453fe6aa9d66)
- Changed: eval reports now use an explicit token budget. (6246811cf02e)
- Fixed: made task inspection resolve compact short task ids through the queue index. (600c5fb2e61b)
- Fixed: AIDE Lite selftest fixture now includes Q28 policy files when Q28 golden tasks run. (0fb6bb2872d7)
- Fixed: excluded AIDE-local Q30 branch-policy artifacts from portable pack truth. (0e62caef186f)
- Fixed: imported target Git policy no longer fails solely because target-local helper plans have not been generated yet. (802052185200)
- Fixed: Q31 governance validation no longer rejects target-style repos that do not contain a source export pack. (7119f14dbdba)
- Fixed: Removed stale generated-manifest validation drift. (84c459505c82)
- Fixed: Resolved the generated-manifest drift warning. (79da4f6c876c)
- Fixed: stale queue blocker guidance no longer appears in Harness doctor or self-check. (6246811cf02e)
- Fixed: AIDE Lite validation no longer reports near-budget ledger entries as warnings. (6246811cf02e)
- Docs: documented Q27 commit, changelog, and WorkUnit recovery workflows. (0de5071ded87)
- Docs: documented Q28 Git workflow policy, branch roles, and promotion gates. (c305b581855a)
- Docs: documented Q29 helper workflow, dry-run defaults, safety gates, fixture-only mutation tests, and Q30 next phase. (da209850bcd7)
- Docs: record AIDE-specific dev/main branch workflow guidance. (19cb12a346f7)
- Docs: recorded Q31 baseline validation evidence scaffold. (7a15b0ed97dd)
- Docs: Recorded Q31 portable governance export behavior and target sync boundaries. (62d13ad71795)
- Docs: recorded Q31 evidence and target-sync readiness. (ca2cc5a1b559)
- Docs: Documented preview-only release draft workflow and target-pack boundary. (453fe6aa9d66)
- Tests: deterministic Q27 coverage for commit lint, changelog preview, and WorkUnit no-op recovery. (f97d7736d0c0)
- Tests: covered deterministic changelog golden tasks and short-id task recovery fixtures. (600c5fb2e61b)
- Tests: added Q28 branch role, workflow detection, and policy guard coverage. (eaaec3594b8b)
- Tests: added fixture Git coverage for Q29 helper land, promote, prune, dirty, unknown-role, protected-branch, and no-push behavior. (990d9cf0dbdc)
- Tests: recorded fixture Git helper coverage and 20/20 golden task pass. (31bd0b29115c)
- Tests: Q30 test coverage follows in the next commit. (7d4302cf01da)
- Tests: added Q30 AIDE branch policy and branch-plan coverage. (8ae66d532800)
- Tests: keep AIDE Lite selftest aligned with Q30 golden tasks. (778aaadd0afe)
- Tests: added Q30 export-boundary coverage. (0e62caef186f)
- Tests: added Q31 fixture import governance coverage. (b1d2e0f99281)
- Tests: updated safe import expectations for portable docs/reference governance docs. (b1d2e0f99281)
- Tests: Re-ran Q31 fixture import coverage and AIDE Lite selftest. (7119f14dbdba)
- Tests: exported Q31 golden tasks and fixture import coverage. (ca2cc5a1b559)
- Tests: Added Q34 changelog parser and preview output coverage. (160de9a7108a)

## Validation Summary

- 65689f6b0ca2: python3 scripts/aide validate: PASS_WITH_WARNINGS, existing review-gate/generated-manifest warnings.
- 65689f6b0ca2: python3 scripts/aide validate: PASS_WITH_WARNINGS, existing review-gate/generated-manifest warnings.
- 1d9469676f16: python3 scripts/aide validate: PASS_WITH_WARNINGS, existing review-gate/generated-manifest warnings.
- 1d9469676f16: python3 scripts/aide validate: PASS_WITH_WARNINGS, existing review-gate/generated-manifest warnings.
- 8ac68636493c: python3 scripts/aide validate: PASS_WITH_WARNINGS, existing review-gate/generated-manifest warnings.
- 8ac68636493c: python3 scripts/aide validate: PASS_WITH_WARNINGS, existing review-gate/generated-manifest warnings.
- 57b73ba81a94: Baseline validation recorded in Q27 evidence: PASS/WARN as documented.
- 86974c90938c: Structural review of policy anchors: PASS.
- 86974c90938c: Structural review of policy anchors: PASS.
- 2146efa0db8f: py -3 .aide/scripts/aide_lite.py commit check --latest: PASS.

## Known Risks

- 65689f6b0ca2: Q27 remains unimplemented.
- 65689f6b0ca2: Q27 remains unimplemented.
- 1d9469676f16: Q28 remains unimplemented.
- 1d9469676f16: Q28 remains unimplemented.
- 8ac68636493c: Q29 remains unimplemented.
- 8ac68636493c: Q29 remains unimplemented.
- 57b73ba81a94: Q27 policy and tooling are not implemented yet in this commit.
- 86974c90938c: Policy exists before the executable AIDE Lite checker in this commit.
- 86974c90938c: Policy exists before the executable AIDE Lite checker in this commit.
- 2146efa0db8f: Full unit coverage and export-pack sync follow in later commits.

## Follow-up

- 65689f6b0ca2: Repair Q25 pack/local-state baseline, then reopen Q27.
- 65689f6b0ca2: Repair Q25 pack/local-state baseline, then reopen Q27.
- 1d9469676f16: Repair Q25 pack/local-state baseline, then implement Q27, then reopen Q28.
- 1d9469676f16: Repair Q25 pack/local-state baseline, then implement Q27, then reopen Q28.
- 8ac68636493c: Repair Q25 baseline, implement Q27, implement Q28, then reopen Q29.
- 8ac68636493c: Repair Q25 baseline, implement Q27, implement Q28, then reopen Q29.
- 57b73ba81a94: Define commit discipline, WorkUnit recovery policies, AIDE Lite commands, tests, docs, and export-pack sync.
- 86974c90938c: Implement commit, changelog, and task recovery commands plus tests and golden tasks.
- 86974c90938c: Implement commit, changelog, and task recovery commands plus tests and golden tasks.
- 2146efa0db8f: Add tests, golden task definitions, docs, regenerated artifacts, and evidence.

## Warnings

- 8 malformed or legacy commits require review

## Preview Caveat

- This draft is not an official release note and does not create tags or GitHub Releases.
