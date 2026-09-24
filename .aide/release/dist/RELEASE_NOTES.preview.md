# AIDE Release Notes Preview

This is a deterministic preview only. It does not publish a release.

source_range: HEAD latest 50 commits
source_head: 3326868b534d6a514af14c4ca3aabc9dc8230579
preview_only: true

## Highlights

- Security: portable pack provenance no longer trusts Git replacement refs. (b4d949c1ac1f)
- Added: local customization explanation and opt-in import feedback. (98de5ee1531e)
- Added: exact historical message dispositions to the dev source ancestry. (e40aec47dd2d)
- Changed: exact no-publish candidate assets and draft evidence regenerated. (8369ac540e4a)
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
- Fixed: dry-run recovery mutation and project-owned metadata payload boundary. (9b21e183d462)
- Fixed: Windows alias route into project-owned customization metadata. (2b4f5de885a5)
- Fixed: allow accountable AEST historical decisions while retaining strict raw policy results. (7a2305f51894)
- Docs: refresh source-bound local changelog and release-note previews. (671faa232216)
- Docs: bind release summaries to the converged generator source. (566a2c3b8b7d)
- Docs: bind release previews to the hardened metadata generator. (e2ec8925adf7)
- Docs: normalize task evidence formatting. (963dcc7d6ede)
- Docs: bind release summaries to the replacement-safe source checkpoint. (7863891e581d)
- Docs: bind release summaries to the paired-preview fail-closed repair. (1397b703a9c1)
- Docs: bind the repaired release-integrity candidate and its exact qualification evidence for review. (853d1c7a8486)
- Docs: refresh preview-only release text for the combined source. (66ef462c2b1b)
- Tests: require validation to preserve all generated release bytes. (edcd591a268b)
- Tests: added JSON/Markdown mismatch and malformed JSON cases. (6cbd104cb048)
- Tests: add official-shape and adversarial selector coverage. (7e56ad751615)
- Tests: cover source-change concealment through git replace. (b4d949c1ac1f)

## Validation Summary

- 671faa232216: PASS: changelog preview reports 50 commits, 0 malformed commits, and 47 highlights.
- edcd591a268b: PASS: 16 Q47 release-bundle tests.
- edcd591a268b: PASS: 16 Q47 release-bundle tests.
- 566a2c3b8b7d: PASS: changelog preview generation and git diff checks.
- 8369ac540e4a: PASS: 57 adjacent governance, export/import, Q47, and Q48 tests.
- 8369ac540e4a: PASS: 57 adjacent governance, export/import, Q47, and Q48 tests.
- 2819a63e794e: PASS: release validate, draft, and draft-validate.
- 6cbd104cb048: PASS: 17 Q47 release-bundle tests.
- 6cbd104cb048: PASS: 17 Q47 release-bundle tests.
- e2ec8925adf7: PASS: changelog preview generation and git diff checks.

## Known Risks

- 671faa232216: Preview outputs remain non-publishing and do not authorize a tag or release.
- edcd591a268b: Previously regenerated artifacts are obsolete and will be deterministically replaced from the new clean source.
- edcd591a268b: Previously regenerated artifacts are obsolete and will be deterministically replaced from the new clean source.
- 566a2c3b8b7d: These files remain preview-only and do not authorize publication.
- 8369ac540e4a: Independent exact-commit rereview and dev integration remain pending.
- 8369ac540e4a: Independent exact-commit rereview and dev integration remain pending.
- 2819a63e794e: Independent exact-commit rereview remains pending.
- 6cbd104cb048: Portable artifacts and source-bound previews must be regenerated from this newer source commit.
- 6cbd104cb048: Portable artifacts and source-bound previews must be regenerated from this newer source commit.
- e2ec8925adf7: Preview files remain non-publishing and authorize no release effect.

## Follow-up

- 671faa232216: Export this clean commit, rebuild final local artifacts, and validate their exact metadata closure.
- edcd591a268b: Refresh source-bound previews and regenerate the export, bundle, draft, and consumer evidence.
- edcd591a268b: Refresh source-bound previews and regenerate the export, bundle, draft, and consumer evidence.
- 566a2c3b8b7d: Regenerate and qualify exact export, archive, and draft bytes from this clean commit.
- 8369ac540e4a: Obtain fresh Sol review; integrate the exact accepted candidate into dev and revalidate the combined tree.
- 8369ac540e4a: Obtain fresh Sol review; integrate the exact accepted candidate into dev and revalidate the combined tree.
- 2819a63e794e: Review this exact closure commit and integrate it into dev if accepted.
- 6cbd104cb048: Refresh previews, rebuild exact artifacts, rerun consumer and canonical validation, and advance independent review.
- 6cbd104cb048: Refresh previews, rebuild exact artifacts, rerun consumer and canonical validation, and advance independent review.
- e2ec8925adf7: Regenerate and qualify the exact portable and release artifacts.

## Warnings

- None.

## Preview Caveat

- This draft is not an official release note and does not create tags or GitHub Releases.
