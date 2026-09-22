# AIDE Release Notes Preview

This is a deterministic preview only. It does not publish a release.

source_range: origin/main..HEAD
source_head: bb308e64f4f23795916b1fe50827ba19043ed893
preview_only: true

## Highlights

- Security: refused Windows 8.3 aliases at the disposable distribution fixture boundary. (64979977922a)
- Security: independently qualified exact-name enforcement for Windows fixture paths. (6cb0a9ac8856)
- Security: Reject Windows 8.3 aliases and other unsafe fixture paths before destination mutation. (bb689227c6a6)
- Security: Integrate reviewed Windows short-name alias refusal into the dev line. (cc85be9c472a)
- Security: Preserve checksum, forbidden-path, and no-publish validation on regenerated archives. (da1051793d4c)
- Security: Record release metadata integrity defects before artifact integration. (4c0da8974daa)
- Added: reusable regressions and explicit candidate boundaries. (e73ac0b269df)
- Added: ownership-aware and interruption-visible AIDE Lite pack updates. (9161d9512738)
- Added: ownership-aware and interruption-aware updates from delivered AIDE Lite packs. (09158bb2a8e1)
- Added: integrate the protected broker foundation and bounded Windows host support into the dev candidate. (091382e81f08)
- Added: land the protected broker and bounded Windows host foundation on dev. (bed5a57aed4f)
- Added: preserve and integrate the published broker runtime line on dev. (c6fdc754844c)
- Added: bounded qualification path for distribution fixture portability. (f737f9199931)
- Added: Admit deterministic release metadata integrity repair. (5ad6aa979971)
- Changed: bind current GitHub target controls and explicit hosted-effect blockers. (75da33108995)
- Changed: refresh local AIDE Lite delivery artifacts with safe update support. (e8c4bbe7d4ab)
- Changed: refresh portable and local release artifacts for the integrated broker-era dev source. (f6ae36e8074b)
- Changed: qualified distribution fixture portability hardening on the full Windows checkout. (36fa64e011b5)
- Changed: Begin commit-bound portable artifact refresh after portability integration. (c730eac44202)
- Changed: Refresh portable artifacts for the integrated Windows path-hardening source. (da1051793d4c)
- Fixed: fixture path portability and preservation defects. (e73ac0b269df)
- Fixed: extracted AIDE Lite archives can validate and safely import without the source checkout. (aa3c8d14b55e)
- Fixed: generated pack provenance now distinguishes clean source from generator-created output changes. (5400f53bc71b)
- Fixed: release provenance now describes source state rather than generator-created output churn. (ffd24f67ba15)
- Fixed: release provenance remains truthful when a clean export pack is an uncommitted generated output. (780312f9ad08)
- Fixed: downloadable AIDE Lite candidates now have closed identities and source-independent safe import. (80746a3ca547)
- Fixed: committed release artifacts retain valid clean-source provenance without accepting stale portable inputs. (4f80611776b7)
- Fixed: the qualified portable candidate now includes post-build provenance validation. (db8cd16279e0)
- Fixed: dev now carries source-independent portable pack import and closed archive identities. (b35394ae939c)
- Fixed: preserve target-authored AGENTS.md bytes around portable guidance. (31bd91bd10ed)
- Fixed: ship exact target-authored guidance preservation in update artifacts. (b1f97c5f3084)
- Fixed: bind release preview checksums to committed portable provenance. (3f1bc120a10c)
- Fixed: land clean post-broker portable and local release provenance on dev. (088b20ba76ae)
- Fixed: refresh and stabilize portable and local release provenance after integration. (c6fdc754844c)
- Fixed: distribution fixture path and preservation boundaries are present on the current-dev candidate. (7aab31bc1bc7)
- Fixed: Bind preview release metadata to committed portability artifact provenance. (38fe712810b8)
- Fixed: release metadata now binds final eligible bytes and the exported source identity. (7bb41079e11f)
- Fixed: release preview binding now matches the generator's complete output set. (bb308e64f4f2)
- Docs: add the immutable expected-head source checkpoint receipt. (045952d757d0)
- Docs: retain exact implementation scope, effect contracts, and qualification boundaries. (091382e81f08)
- Docs: publish exact effect contracts and qualification limits. (bed5a57aed4f)
- Tests: define delivered-pack update acceptance regressions. (69e363bc71be)
- Tests: land broker, provider, GitHub, host, image, PE, and security regressions. (bed5a57aed4f)
- Tests: requalify extracted archives, updates, checksums, and no-publish boundaries. (f6ae36e8074b)
- Tests: retain extracted consumer and no-publish qualification evidence. (088b20ba76ae)
- Tests: added stale-preview, file-set, hash, size, and cross-checkout regressions. (7bb41079e11f)
- Tests: added positive projection and unrelated-change refusal coverage. (bb308e64f4f2)

## Validation Summary

- 045952d757d0: PASS: workunit validate checked 353 queue tasks and objects.
- 75da33108995: PASS: authenticated read-only queries ran under BLACKGLASS-WIN1\\Jules as Julesc013.
- e73ac0b269df: PASS: all three captured baseline Git blob identities verified.
- e73ac0b269df: PASS: all three captured baseline Git blob identities verified.
- aa3c8d14b55e: PASS: 46 focused and adjacent tests; fresh disposable import wrote 814 files with zero conflicts; target-local doctor passed; repeated archives were byte-identical.
- 5400f53bc71b: PASS: export/import 16 tests; release bundle 9 tests; Python compilation and diff checks.
- ffd24f67ba15: PASS: Q47 release bundle 10 tests; Python compilation and diff checks.
- 780312f9ad08: PASS: Q47 release bundle 10 tests; focused clean-pack regression; Python compilation and diff checks.
- 80746a3ca547: PASS: 48 focused tests, release validation, release-draft validation, repository validation, two fresh consumer imports, two target-local doctor runs, and repeat hash checks.
- 4f80611776b7: PASS: export/import 17 tests, focused stale-pack regression, Python compilation, and diff checks.

## Known Risks

- 045952d757d0: This receipt is not hosted target acceptance and authorizes no GitHub mutation or settings change.
- 75da33108995: No current target policy, workflow, or restricted broker principal can support hosted adversarial acceptance.
- e73ac0b269df: This is an intake-backed source candidate pending canonical child-WorkUnit admission and full-checkout review.
- e73ac0b269df: This is an intake-backed source candidate pending canonical child-WorkUnit admission and full-checkout review.
- aa3c8d14b55e: Generated release artifacts still need clean-source regeneration and candidate qualification before integration or publication.
- 5400f53bc71b: Release artifacts still require regeneration and final consumer qualification from this commit.
- ffd24f67ba15: Final export and release artifacts remain to be generated and qualified from this commit.
- 780312f9ad08: Exact generated artifacts and consumer canaries remain to be committed and integrated.
- 80746a3ca547: This is a local no-publish candidate; main promotion, stable version selection, tag, upload, and public release remain separately gated.
- 4f80611776b7: Final pack and archive bytes must be regenerated from this validator commit before integration.

## Follow-up

- 045952d757d0: Observe and independently review the exact current target policy, workflow provenance, principal permissions, and bypass state.
- 75da33108995: Prepare and independently review an exact non-mutating desired configuration with real app/principal identities before any apply action.
- e73ac0b269df: Materialize the bounded child WorkUnit under the current programme, reproduce in a complete checkout, run the distribution/full validation matrix and native profiles, and obtain independent review before integration.
- e73ac0b269df: Materialize the bounded child WorkUnit under the current programme, reproduce in a complete checkout, run the distribution/full validation matrix and native profiles, and obtain independent review before integration.
- aa3c8d14b55e: Regenerate export and release artifacts from this commit, rerun consumer qualification, and prepare the exact task-to-dev candidate.
- 5400f53bc71b: Generate the portable pack and archives from clean committed source, qualify exact bytes, and publish the task branch.
- ffd24f67ba15: Commit the clean export pack, then generate and qualify exact release archives from that clean state.
- 780312f9ad08: Generate the final pack and archives, validate exact hashes, close the WorkUnit, and publish the candidate branch.
- 80746a3ca547: Publish the task branch, validate the exact task-to-dev candidate, and fast-forward dev when helper gates pass.
- 4f80611776b7: Regenerate, rerun exact consumer and repository qualification, then publish and integrate the candidate.

## Warnings

- None.

## Preview Caveat

- This draft is not an official release note and does not create tags or GitHub Releases.
