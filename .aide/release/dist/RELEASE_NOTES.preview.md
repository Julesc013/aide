# AIDE Release Notes Preview

This is a deterministic preview only. It does not publish a release.

source_range: HEAD latest 50 commits
source_head: 4deeed08be90080583183ca5a24597a4a72aedda
preview_only: true

## Highlights

- Security: refused Windows 8.3 aliases at the disposable distribution fixture boundary. (64979977922a)
- Security: bound locally accepted GitHub checks to exact workflow-run provenance without overstating server enforcement. (cb05b135eb0d)
- Security: independently qualified exact-name enforcement for Windows fixture paths. (6cb0a9ac8856)
- Security: Reject Windows 8.3 aliases and other unsafe fixture paths before destination mutation. (bb689227c6a6)
- Security: Integrate reviewed Windows short-name alias refusal into the dev line. (cc85be9c472a)
- Security: Preserve checksum, forbidden-path, and no-publish validation on regenerated archives. (da1051793d4c)
- Security: Record release metadata integrity defects before artifact integration. (4c0da8974daa)
- Security: Preserve fail-closed target qualification review findings before integration. (b8fb89b917c9)
- Security: portable pack provenance no longer trusts Git replacement refs. (b4d949c1ac1f)
- Added: preserve and integrate the published broker runtime line on dev. (c6fdc754844c)
- Added: fail-closed review-only GitHub target-policy contract for the continuous-worker integration broker (bb433bb74f64)
- Added: bounded qualification path for distribution fixture portability. (f737f9199931)
- Added: Admit deterministic release metadata integrity repair. (5ad6aa979971)
- Changed: refresh portable and local release artifacts for the integrated broker-era dev source. (f6ae36e8074b)
- Changed: target-policy queue state now records its exact published review checkpoint (eb4dea3f30ab)
- Changed: qualified distribution fixture portability hardening on the full Windows checkout. (36fa64e011b5)
- Changed: Begin commit-bound portable artifact refresh after portability integration. (c730eac44202)
- Changed: Refresh portable artifacts for the integrated Windows path-hardening source. (da1051793d4c)
- Changed: exact no-publish candidate assets and draft evidence regenerated. (8369ac540e4a)
- Fixed: bind release preview checksums to committed portable provenance. (3f1bc120a10c)
- Fixed: land clean post-broker portable and local release provenance on dev. (088b20ba76ae)
- Fixed: refresh and stabilize portable and local release provenance after integration. (c6fdc754844c)
- Fixed: distribution fixture path and preservation boundaries are present on the current-dev candidate. (7aab31bc1bc7)
- Fixed: GitHub policy planning now binds valid rule bytes, separate principals, exact workflow source, and effective policy state. (9383c2b5e852)
- Fixed: Bind preview release metadata to committed portability artifact provenance. (38fe712810b8)
- Fixed: release metadata now binds final eligible bytes and the exported source identity. (7bb41079e11f)
- Fixed: release preview binding now matches the generator's complete output set. (bb308e64f4f2)
- Fixed: release bundle and validation commands now converge on one deterministic metadata state. (edcd591a268b)
- Fixed: release metadata is internally exact, checkout-independent, source-bound, and byte-stable. (8369ac540e4a)
- Fixed: committed release draft metadata now reflects post-checkpoint pack provenance exactly. (2819a63e794e)
- Fixed: preview publication gating now binds both generated representations and fails closed on malformed metadata. (6cbd104cb048)
- Fixed: documented workflow-run path@ref provenance is parsed and bound to the admitted source. (7e56ad751615)
- Fixed: produce replacement-safe, checkout-neutral local release artifacts for exact rereview. (dd1f39f39f3d)
- Fixed: close the deterministic post-commit provenance projection across local bundle and release-draft records. (198a87d29238)
- Fixed: align durable release qualification records with the policy-compliant local commit identities. (9f4bbc0a7744)
- Fixed: fail closed when either release-preview JSON identity is absent. (f147c9059e8b)
- Fixed: align target-policy comparison with GitHub branch-rules endpoint semantics. (e378d38e0c51)
- Fixed: deliver release artifacts that require paired preview identities and refuse missing JSON sources. (7897f7deb80c)
- Fixed: project paired-preview release provenance from actual artifact checkpoint 7897f7de. (d6642c3d81f6)
- Fixed: integrate endpoint-shaped effective GitHub rule comparison into the dev source. (6a581dbcfbd5)
- Docs: refresh source-bound local changelog and release-note previews. (671faa232216)
- Docs: bind release summaries to the converged generator source. (566a2c3b8b7d)
- Docs: bind release previews to the hardened metadata generator. (e2ec8925adf7)
- Docs: normalize task evidence formatting. (963dcc7d6ede)
- Docs: bind release summaries to the replacement-safe source checkpoint. (7863891e581d)
- Docs: bind release summaries to the paired-preview fail-closed repair. (1397b703a9c1)
- Docs: bind the repaired release-integrity candidate and its exact qualification evidence for review. (853d1c7a8486)
- Tests: requalify extracted archives, updates, checksums, and no-publish boundaries. (f6ae36e8074b)
- Tests: retain extracted consumer and no-publish qualification evidence. (088b20ba76ae)
- Tests: added stale-preview, file-set, hash, size, and cross-checkout regressions. (7bb41079e11f)
- Tests: added positive projection and unrelated-change refusal coverage. (bb308e64f4f2)
- Tests: require validation to preserve all generated release bytes. (edcd591a268b)
- Tests: added JSON/Markdown mismatch and malformed JSON cases. (6cbd104cb048)
- Tests: add official-shape and adversarial selector coverage. (7e56ad751615)
- Tests: cover source-change concealment through git replace. (b4d949c1ac1f)

## Validation Summary

- b3e5c7aa2a17: PASS: intent packet validation.
- f6ae36e8074b: PASS: export-pack and pack-status with 826 files, 829 checksums, and zero provenance or boundary problems.
- f6ae36e8074b: PASS: export-pack and pack-status with 826 files, 829 checksums, and zero provenance or boundary problems.
- 3f1bc120a10c: PASS: release bundle and draft generators.
- 3f1bc120a10c: PASS: release bundle and draft generators.
- 088b20ba76ae: PASS: exact staged tree equals published task tree 2bb4a151d57fa250c244e6183509efdf48ea9fe1.
- 088b20ba76ae: PASS: exact staged tree equals published task tree 2bb4a151d57fa250c244e6183509efdf48ea9fe1.
- c6fdc754844c: PASS: both task inspections classify complete with no missing evidence.
- c6fdc754844c: PASS: both task inspections classify complete with no missing evidence.
- c6fdc754844c: PASS: both task inspections classify complete with no missing evidence.

## Known Risks

- b3e5c7aa2a17: Generated path scope and byte changes are unknown until deterministic regeneration.
- f6ae36e8074b: These are local no-publish artifacts and a preview-only release draft, not a public stable release.
- f6ae36e8074b: These are local no-publish artifacts and a preview-only release draft, not a public stable release.
- 3f1bc120a10c: Artifacts remain local and no-publish; no public release is claimed.
- 3f1bc120a10c: Artifacts remain local and no-publish; no public release is claimed.
- 088b20ba76ae: This is still a local no-publish bundle and preview draft, not a tagged or uploaded stable release.
- 088b20ba76ae: This is still a local no-publish bundle and preview draft, not a tagged or uploaded stable release.
- c6fdc754844c: Operational broker completion, restricted credentials, hosted races, protected-host closeout, main promotion, tags, upload, and public release remain open gates.
- c6fdc754844c: Operational broker completion, restricted credentials, hosted races, protected-host closeout, main promotion, tags, upload, and public release remain open gates.
- c6fdc754844c: Operational broker completion, restricted credentials, hosted races, protected-host closeout, main promotion, tags, upload, and public release remain open gates.

## Follow-up

- b3e5c7aa2a17: Publish admission, regenerate export and local release artifacts from clean source, and run exact consumer and canonical checks.
- f6ae36e8074b: Publish this task candidate, land it into dev, rerun post-landing validation, and close the broker integration and pack-refresh tasks.
- f6ae36e8074b: Publish this task candidate, land it into dev, rerun post-landing validation, and close the broker integration and pack-refresh tasks.
- 3f1bc120a10c: Publish the task candidate, verify clean post-commit validation, and land the exact branch into dev.
- 3f1bc120a10c: Publish the task candidate, verify clean post-commit validation, and land the exact branch into dev.
- 088b20ba76ae: Run post-commit canonical validation, push dev, observe refs, and close the pack-refresh and parent integration tasks.
- 088b20ba76ae: Run post-commit canonical validation, push dev, observe refs, and close the pack-refresh and parent integration tasks.
- c6fdc754844c: Continue AIDE-CW-INTEGRATION-BROKER-01, isolated-host, and GitHub target qualification from their integrated checkpoints; handle main and release only through exact retained gates.
- c6fdc754844c: Continue AIDE-CW-INTEGRATION-BROKER-01, isolated-host, and GitHub target qualification from their integrated checkpoints; handle main and release only through exact retained gates.
- c6fdc754844c: Continue AIDE-CW-INTEGRATION-BROKER-01, isolated-host, and GitHub target qualification from their integrated checkpoints; handle main and release only through exact retained gates.

## Warnings

- None.

## Preview Caveat

- This draft is not an official release note and does not create tags or GitHub Releases.
