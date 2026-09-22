# AIDE Release Notes Preview

This is a deterministic preview only. It does not publish a release.

source_range: origin/main..HEAD
source_head: b4d949c1ac1f7481a56c763bdb41582291d477c9
preview_only: true

## Highlights

- Security: refused Windows 8.3 aliases at the disposable distribution fixture boundary. (64979977922a)
- Security: independently qualified exact-name enforcement for Windows fixture paths. (6cb0a9ac8856)
- Security: Reject Windows 8.3 aliases and other unsafe fixture paths before destination mutation. (bb689227c6a6)
- Security: Integrate reviewed Windows short-name alias refusal into the dev line. (cc85be9c472a)
- Security: Preserve checksum, forbidden-path, and no-publish validation on regenerated archives. (da1051793d4c)
- Security: Record release metadata integrity defects before artifact integration. (4c0da8974daa)
- Security: portable pack provenance no longer trusts Git replacement refs. (b4d949c1ac1f)
- Added: ownership-aware and interruption-visible AIDE Lite pack updates. (9161d9512738)
- Added: ownership-aware and interruption-aware updates from delivered AIDE Lite packs. (09158bb2a8e1)
- Added: integrate the protected broker foundation and bounded Windows host support into the dev candidate. (091382e81f08)
- Added: land the protected broker and bounded Windows host foundation on dev. (bed5a57aed4f)
- Added: preserve and integrate the published broker runtime line on dev. (c6fdc754844c)
- Added: bounded qualification path for distribution fixture portability. (f737f9199931)
- Added: Admit deterministic release metadata integrity repair. (5ad6aa979971)
- Changed: refresh local AIDE Lite delivery artifacts with safe update support. (e8c4bbe7d4ab)
- Changed: refresh portable and local release artifacts for the integrated broker-era dev source. (f6ae36e8074b)
- Changed: qualified distribution fixture portability hardening on the full Windows checkout. (36fa64e011b5)
- Changed: Begin commit-bound portable artifact refresh after portability integration. (c730eac44202)
- Changed: Refresh portable artifacts for the integrated Windows path-hardening source. (da1051793d4c)
- Changed: exact no-publish candidate assets and draft evidence regenerated. (8369ac540e4a)
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
- Fixed: release bundle and validation commands now converge on one deterministic metadata state. (edcd591a268b)
- Fixed: release metadata is internally exact, checkout-independent, source-bound, and byte-stable. (8369ac540e4a)
- Fixed: committed release draft metadata now reflects post-checkpoint pack provenance exactly. (2819a63e794e)
- Fixed: preview publication gating now binds both generated representations and fails closed on malformed metadata. (6cbd104cb048)
- Docs: retain exact implementation scope, effect contracts, and qualification boundaries. (091382e81f08)
- Docs: publish exact effect contracts and qualification limits. (bed5a57aed4f)
- Docs: refresh source-bound local changelog and release-note previews. (671faa232216)
- Docs: bind release summaries to the converged generator source. (566a2c3b8b7d)
- Docs: bind release previews to the hardened metadata generator. (e2ec8925adf7)
- Tests: define delivered-pack update acceptance regressions. (69e363bc71be)
- Tests: land broker, provider, GitHub, host, image, PE, and security regressions. (bed5a57aed4f)
- Tests: requalify extracted archives, updates, checksums, and no-publish boundaries. (f6ae36e8074b)
- Tests: retain extracted consumer and no-publish qualification evidence. (088b20ba76ae)
- Tests: added stale-preview, file-set, hash, size, and cross-checkout regressions. (7bb41079e11f)
- Tests: added positive projection and unrelated-change refusal coverage. (bb308e64f4f2)
- Tests: require validation to preserve all generated release bytes. (edcd591a268b)
- Tests: added JSON/Markdown mismatch and malformed JSON cases. (6cbd104cb048)
- Tests: cover source-change concealment through git replace. (b4d949c1ac1f)

## Validation Summary

- 4f80611776b7: PASS: export/import 17 tests, focused stale-pack regression, Python compilation, and diff checks.
- db8cd16279e0: PASS: pack/release/repository validation; ZIP and tar.gz isolated imports; two target-local doctor runs; repeat archive hashes.
- dd8e1c226006: PASS: pack status, release validation, draft validation, and repository validation.
- b35394ae939c: PASS: pre-merge 49 focused tests, repository validation, two exact archive canaries, and structured commit range.
- 8e1e9a9d724d: PASS: post-merge Q47/Q48, pack provenance, repository validation, remote dev observation, and closeout diff checks.
- a2ba43624bf9: PASS: helper landing plan, closeout repository validation, and structured commit policy.
- 34c49601964d: PASS: git diff --check.
- 69e363bc71be: PASS: 17 existing export/import tests remain green.
- 9161d9512738: PASS: 24 export/import tests.
- e8c4bbe7d4ab: PASS: export pack boundary and checksum validation.

## Known Risks

- 4f80611776b7: Final pack and archive bytes must be regenerated from this validator commit before integration.
- db8cd16279e0: This remains a local candidate; main, tagging, upload, and public publication retain exact review gates.
- dd8e1c226006: No publication occurred; task-to-dev integration is still pending exact helper validation.
- b35394ae939c: Main promotion, version selection, tag, upload, and public release remain separately gated.
- 8e1e9a9d724d: Main promotion, stable version selection, tag, upload, publication, and remaining product work are still open.
- a2ba43624bf9: Main, tag, upload, publication, and remaining stable-release work remain gated.
- 34c49601964d: No target, release, integration, or publication effect occurred.
- 69e363bc71be: Tests use disposable temporary repositories and perform no live target mutation.
- 9161d9512738: Qualification remains limited to disposable consumers; semantic merge and live target rollout remain gated.
- e8c4bbe7d4ab: Artifacts are local candidates only; no tag, upload, release, or main mutation occurred.

## Follow-up

- 4f80611776b7: Regenerate, rerun exact consumer and repository qualification, then publish and integrate the candidate.
- db8cd16279e0: Validate the committed artifact state, publish the task branch, and integrate the exact candidate to dev.
- dd8e1c226006: Prove validation is idempotent, publish the task branch, and integrate the exact candidate to dev.
- b35394ae939c: Run post-merge validation, push exact dev, and close the child WorkUnit with observed refs.
- 8e1e9a9d724d: Integrate this closeout record to dev and select the next bounded stable implementation child.
- a2ba43624bf9: Validate and push exact dev, then continue the next bounded product slice.
- 34c49601964d: Add failing lifecycle regressions before implementation.
- 69e363bc71be: Implement the portable receipt, plan binding, and interruption journal.
- 9161d9512738: Run adjacent suites and qualify artifacts generated from a clean source commit.
- e8c4bbe7d4ab: Revalidate committed artifact provenance and the exact archive bytes.

## Warnings

- None.

## Preview Caveat

- This draft is not an official release note and does not create tags or GitHub Releases.
