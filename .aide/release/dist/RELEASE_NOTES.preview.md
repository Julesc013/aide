# AIDE Release Notes Preview

This is a deterministic preview only. It does not publish a release.

source_range: HEAD latest 50 commits
source_head: 98de5ee1531e3d71f6f003f8bc98bf2a6b8bf23b
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
- Added: bounded qualification path for distribution fixture portability. (f737f9199931)
- Added: Admit deterministic release metadata integrity repair. (5ad6aa979971)
- Added: local customization explanation and opt-in import feedback. (98de5ee1531e)
- Changed: target-policy queue state now records its exact published review checkpoint (eb4dea3f30ab)
- Changed: qualified distribution fixture portability hardening on the full Windows checkout. (36fa64e011b5)
- Changed: Begin commit-bound portable artifact refresh after portability integration. (c730eac44202)
- Changed: Refresh portable artifacts for the integrated Windows path-hardening source. (da1051793d4c)
- Changed: exact no-publish candidate assets and draft evidence regenerated. (8369ac540e4a)
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
- Fixed: refresh local export and release provenance for combined target source. (cda504b9a546)
- Fixed: bind local release metadata to the committed combined-source artifact ancestry. (d4bd4938fa43)
- Docs: refresh source-bound local changelog and release-note previews. (671faa232216)
- Docs: bind release summaries to the converged generator source. (566a2c3b8b7d)
- Docs: bind release previews to the hardened metadata generator. (e2ec8925adf7)
- Docs: normalize task evidence formatting. (963dcc7d6ede)
- Docs: bind release summaries to the replacement-safe source checkpoint. (7863891e581d)
- Docs: bind release summaries to the paired-preview fail-closed repair. (1397b703a9c1)
- Docs: bind the repaired release-integrity candidate and its exact qualification evidence for review. (853d1c7a8486)
- Docs: refresh preview-only release text for the combined source. (66ef462c2b1b)
- Tests: added stale-preview, file-set, hash, size, and cross-checkout regressions. (7bb41079e11f)
- Tests: added positive projection and unrelated-change refusal coverage. (bb308e64f4f2)
- Tests: require validation to preserve all generated release bytes. (edcd591a268b)
- Tests: added JSON/Markdown mismatch and malformed JSON cases. (6cbd104cb048)
- Tests: add official-shape and adversarial selector coverage. (7e56ad751615)
- Tests: cover source-change concealment through git replace. (b4d949c1ac1f)

## Validation Summary

- eb4dea3f30ab: PASS: remote task ref equals bb433bb74f645e0904ca34bf3af38516ae05a7ad
- f737f9199931: PASS: exact candidate commit, tree, parent, diff, and commit-range checks.
- 7aab31bc1bc7: PASS: source commit range and diff checks before merge.
- 9bba1cecaec8: PASS: 44 focused GitHub observation/target-policy tests
- 9383c2b5e852: PASS: 135 affected tests; 134 passed and one Windows symlink test skipped.
- 36fa64e011b5: PASS WITH SKIPS: 156 adjacent distribution tests; 148 passed and eight skipped.
- 64979977922a: PASS WITH SKIPS: 126 focused tests; 118 passed and eight skipped.
- cb05b135eb0d: PASS: 46 target-observation, 21 PR-observation, 19 HTTP, and 12 provider-bridge tests.
- 6cb0a9ac8856: PASS WITH SKIPS: 126 focused tests; 118 passed and eight skipped.
- bb689227c6a6: PASS: candidate range commit policy check for all six commits.

## Known Risks

- eb4dea3f30ab: broker principal and workflow/check identities remain unresolved
- f737f9199931: Source acceptance remains pending Windows tests and independent exact-commit review.
- 7aab31bc1bc7: Combined-tree behavior remains unqualified until the recorded Windows and adjacent suites pass.
- 9bba1cecaec8: no product source was edited
- 9383c2b5e852: The repaired exact source still requires superseding independent review.
- 36fa64e011b5: Independent exact-commit review is pending.
- 64979977922a: Exact repair rereview remains pending.
- cb05b135eb0d: Same-app and same-check-name collision exclusion remains unsupported at the destination boundary.
- 6cb0a9ac8856: Privilege-dependent symlink and Windows FIFO behavior remain unqualified.
- bb689227c6a6: Post-merge combined-tree tests and portable artifact provenance refresh remain required.

## Follow-up

- eb4dea3f30ab: obtain independent review after resolving exact identities
- f737f9199931: Merge the exact source commit with both histories preserved and validate the combined tree.
- 7aab31bc1bc7: Run focused, adjacent, and canonical validation, then obtain independent exact-commit review.
- 9bba1cecaec8: remediate F-01 through F-04 and submit a new exact-source checkpoint for independent review
- 9383c2b5e852: Publish the repair and obtain independent exact-commit rereview before any target effect packet.
- 36fa64e011b5: Obtain independent review, integrate the exact candidate to dev, then refresh and qualify portable artifacts.
- 64979977922a: Rereview this exact repair, integrate the passing candidate to dev, and refresh commit-bound portable artifacts.
- cb05b135eb0d: Obtain superseding independent review, then integrate source-only guarantees while keeping hosted effects blocked.
- 6cb0a9ac8856: Publish this reviewed closeout, merge the exact candidate to dev, and refresh delivered artifacts.
- bb689227c6a6: Run the focused and adjacent suites on the merged tree, record exact evidence, and regenerate commit-bound portable artifacts.

## Warnings

- None.

## Preview Caveat

- This draft is not an official release note and does not create tags or GitHub Releases.
