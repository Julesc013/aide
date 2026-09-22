# AIDE Release Notes Preview

This is a deterministic preview only. It does not publish a release.

source_range: HEAD latest 50 commits
source_head: f147c9059e8b42ea0f4618a45d306080f300e507
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
- Fixed: produce replacement-safe, checkout-neutral local release artifacts for exact rereview. (dd1f39f39f3d)
- Fixed: close the deterministic post-commit provenance projection across local bundle and release-draft records. (198a87d29238)
- Fixed: align durable release qualification records with the policy-compliant local commit identities. (9f4bbc0a7744)
- Fixed: fail closed when either release-preview JSON identity is absent. (f147c9059e8b)
- Docs: retain exact implementation scope, effect contracts, and qualification boundaries. (091382e81f08)
- Docs: publish exact effect contracts and qualification limits. (bed5a57aed4f)
- Docs: refresh source-bound local changelog and release-note previews. (671faa232216)
- Docs: bind release summaries to the converged generator source. (566a2c3b8b7d)
- Docs: bind release previews to the hardened metadata generator. (e2ec8925adf7)
- Docs: bind release summaries to the replacement-safe source checkpoint. (7863891e581d)
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

- a2ba43624bf9: PASS: helper landing plan, closeout repository validation, and structured commit policy.
- 34c49601964d: PASS: git diff --check.
- 69e363bc71be: PASS: 17 existing export/import tests remain green.
- 9161d9512738: PASS: 24 export/import tests.
- e8c4bbe7d4ab: PASS: export pack boundary and checksum validation.
- 3ef2372d7cdf: PASS: release bundle and committed-state validation.
- 31bd91bd10ed: PASS: Python compilation.
- b1f97c5f3084: PASS: 25 export/import tests and 10 Q47 tests.
- 12918667778a: PASS: release bundle and validation.
- dab67d269365: PASS: py -3 .aide/scripts/aide_lite.py test.

## Known Risks

- a2ba43624bf9: Main, tag, upload, publication, and remaining stable-release work remain gated.
- 34c49601964d: No target, release, integration, or publication effect occurred.
- 69e363bc71be: Tests use disposable temporary repositories and perform no live target mutation.
- 9161d9512738: Qualification remains limited to disposable consumers; semantic merge and live target rollout remain gated.
- e8c4bbe7d4ab: Artifacts are local candidates only; no tag, upload, release, or main mutation occurred.
- 3ef2372d7cdf: The candidate remains local and preview-only; publication gates are unchanged.
- 31bd91bd10ed: UTF-8 remains the admitted portable text encoding; non-UTF-8 target guidance is refused.
- b1f97c5f3084: Artifacts remain local preview candidates with no publish authority.
- 12918667778a: Candidate remains preview-only and is not a stable release publication.
- dab67d269365: Real target adoption, semantic merge, automatic recovery, main promotion, tags, upload, and publication remain outside this task.

## Follow-up

- a2ba43624bf9: Validate and push exact dev, then continue the next bounded product slice.
- 34c49601964d: Add failing lifecycle regressions before implementation.
- 69e363bc71be: Implement the portable receipt, plan binding, and interruption journal.
- 9161d9512738: Run adjacent suites and qualify artifacts generated from a clean source commit.
- e8c4bbe7d4ab: Revalidate committed artifact provenance and the exact archive bytes.
- 3ef2372d7cdf: Re-run read-only validation without regenerating bundle identity.
- 31bd91bd10ed: Re-run the full importer suite and rebuild exact delivery artifacts.
- b1f97c5f3084: Stabilize committed-state release evidence and run final validation.
- 12918667778a: Run final read-only validation, close the task, publish the task branch, and prepare dev integration.
- dab67d269365: Publish the exact task head, run the landing helper, validate the merged candidate on dev, and observe the remote ref.

## Warnings

- None.

## Preview Caveat

- This draft is not an official release note and does not create tags or GitHub Releases.
