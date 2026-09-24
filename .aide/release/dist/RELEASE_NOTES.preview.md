# AIDE Release Notes Preview

This is a deterministic preview only. It does not publish a release.

source_range: HEAD latest 50 commits
source_head: ab17fd664159c46fa40e4683f8a4276c452a34a1
preview_only: true

## Highlights

- Security: portable pack provenance no longer trusts Git replacement refs. (b4d949c1ac1f)
- Added: local customization explanation and opt-in import feedback. (98de5ee1531e)
- Added: exact historical message dispositions to the dev source ancestry. (e40aec47dd2d)
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
- Fixed: prevent dirty-source provenance in the local combined artifact projection. (1fa02a8594fe)
- Docs: normalize task evidence formatting. (963dcc7d6ede)
- Docs: bind release summaries to the replacement-safe source checkpoint. (7863891e581d)
- Docs: bind release summaries to the paired-preview fail-closed repair. (1397b703a9c1)
- Docs: bind the repaired release-integrity candidate and its exact qualification evidence for review. (853d1c7a8486)
- Docs: refresh preview-only release text for the combined source. (66ef462c2b1b)
- Tests: add official-shape and adversarial selector coverage. (7e56ad751615)
- Tests: cover source-change concealment through git replace. (b4d949c1ac1f)

## Validation Summary

- 7e56ad751615: PASS: 48 focused GitHub observation/policy tests.
- 7e56ad751615: PASS: 48 focused GitHub observation/policy tests.
- 7e56ad751615: PASS: 48 focused GitHub observation/policy tests.
- 963dcc7d6ede: PASS: git diff --check after this correction.
- b4d949c1ac1f: PASS: adversarial export provenance regression.
- b4d949c1ac1f: PASS: adversarial export provenance regression.
- 7863891e581d: PASS: changelog preview generation and git diff checks.
- dd1f39f39f3d: PASS: 58 adjacent tests, canonical validate and doctor, two delivered-byte consumer canaries, and 44-file repeatability comparison.
- 198a87d29238: PASS: pack-status reports PASS_SOURCE_ANCESTOR.
- 9f4bbc0a7744: PASS: commit range 7863891e..198a87d2.

## Known Risks

- 7e56ad751615: Workflow provenance remains locally checked and monitored, not destination-side source enforcement.
- 7e56ad751615: Workflow provenance remains locally checked and monitored, not destination-side source enforcement.
- 7e56ad751615: Workflow provenance remains locally checked and monitored, not destination-side source enforcement.
- 963dcc7d6ede: None; this is a documentation-only whitespace correction.
- b4d949c1ac1f: Generated export and release artifacts must be rebuilt from the new source.
- b4d949c1ac1f: Generated export and release artifacts must be rebuilt from the new source.
- 7863891e581d: The preview remains local and non-publishing.
- dd1f39f39f3d: This first artifact checkpoint still requires the complete post-commit provenance projection and independent exact-commit rereview.
- 198a87d29238: Independent review is still required before dev integration.
- 9f4bbc0a7744: Independent exact-commit rereview and dev integration remain pending.

## Follow-up

- 7e56ad751615: Obtain independent rereview; retain all target configuration and hosted-effect gates.
- 7e56ad751615: Obtain independent rereview; retain all target configuration and hosted-effect gates.
- 7e56ad751615: Obtain independent rereview; retain all target configuration and hosted-effect gates.
- 963dcc7d6ede: Validate the exact two-commit candidate and publish it for independent rereview.
- b4d949c1ac1f: Refresh source-bound previews, regenerate final artifacts, and obtain exact independent rereview.
- b4d949c1ac1f: Refresh source-bound previews, regenerate final artifacts, and obtain exact independent rereview.
- 7863891e581d: Regenerate, qualify, commit, and independently rereview the final artifact candidate.
- dd1f39f39f3d: Run and commit the complete post-commit bundle, validate, draft, and draft-validate projection; prove a second full cycle is byte-identical; obtain independent rereview.
- 198a87d29238: Replay the complete cycle from this committed candidate, require a clean tree, run canonical and commit checks, push, and obtain independent exact-commit rereview.
- 9f4bbc0a7744: Validate this complete range, push it, and obtain independent exact-commit rereview.

## Warnings

- None.

## Preview Caveat

- This draft is not an official release note and does not create tags or GitHub Releases.
