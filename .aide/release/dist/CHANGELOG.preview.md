# AIDE Changelog Preview

This file is generated from local Git history and is a preview only.

source_range: HEAD latest 50 commits
source_head: 98de5ee1531e3d71f6f003f8bc98bf2a6b8bf23b
commit_count: 50
malformed_count: 0
preview_only: true
release_publishing: false

## Summary

- Added: 3
- Changed: 5
- Fixed: 20
- Security: 9
- Docs: 8
- Tests: 6
- Internal: 7
- Risks: 1

## Added

- bounded qualification path for distribution fixture portability. (f737f9199931 chore(queue): admit fixture portability integration)
- Admit deterministic release metadata integrity repair. (5ad6aa979971 chore(release): admit metadata integrity repair)
- local customization explanation and opt-in import feedback. (98de5ee1531e feat(import): explain downstream customization decisions)

## Changed

- target-policy queue state now records its exact published review checkpoint (eb4dea3f30ab chore(queue): record target-policy source publication)
- qualified distribution fixture portability hardening on the full Windows checkout. (36fa64e011b5 test(distribution): qualify portability candidate)
- Begin commit-bound portable artifact refresh after portability integration. (c730eac44202 chore(distribution): start clean artifact refresh)
- Refresh portable artifacts for the integrated Windows path-hardening source. (da1051793d4c build(distribution): refresh portable artifacts)
- exact no-publish candidate assets and draft evidence regenerated. (8369ac540e4a build(release): qualify deterministic candidate)

## Fixed

- distribution fixture path and preservation boundaries are present on the current-dev candidate. (7aab31bc1bc7 fix(distribution): merge portability source candidate)
- GitHub policy planning now binds valid rule bytes, separate principals, exact workflow source, and effective policy state. (9383c2b5e852 fix(provider): repair target-policy review findings)
- Bind preview release metadata to committed portability artifact provenance. (38fe712810b8 build(distribution): close artifact provenance)
- release metadata now binds final eligible bytes and the exported source identity. (7bb41079e11f fix(release): bind metadata to final artifacts)
- release preview binding now matches the generator's complete output set. (bb308e64f4f2 fix(release): accept complete preview projection)
- release bundle and validation commands now converge on one deterministic metadata state. (edcd591a268b fix(release): converge bundle validation bytes)
- release metadata is internally exact, checkout-independent, source-bound, and byte-stable. (8369ac540e4a build(release): qualify deterministic candidate)
- committed release draft metadata now reflects post-checkpoint pack provenance exactly. (2819a63e794e build(release): close post-commit provenance)
- preview publication gating now binds both generated representations and fails closed on malformed metadata. (6cbd104cb048 fix(release): bind both preview representations)
- documented workflow-run path@ref provenance is parsed and bound to the admitted source. (7e56ad751615 fix(workflow): bind documented path ref)
- produce replacement-safe, checkout-neutral local release artifacts for exact rereview. (dd1f39f39f3d build(release): checkpoint replacement-safe artifacts)
- close the deterministic post-commit provenance projection across local bundle and release-draft records. (198a87d29238 build(release): close committed provenance projection)
- align durable release qualification records with the policy-compliant local commit identities. (9f4bbc0a7744 docs(release): bind final qualification checkpoint)
- fail closed when either release-preview JSON identity is absent. (f147c9059e8b fix(release): require paired preview identities)
- align target-policy comparison with GitHub branch-rules endpoint semantics. (e378d38e0c51 fix(github): compare endpoint-shaped branch rules)
- deliver release artifacts that require paired preview identities and refuse missing JSON sources. (7897f7deb80c build(release): checkpoint paired-preview artifacts)
- project paired-preview release provenance from actual artifact checkpoint 7897f7de. (d6642c3d81f6 build(release): project checkpoint 7897f7de provenance)
- integrate endpoint-shaped effective GitHub rule comparison into the dev source. (6a581dbcfbd5 feat(github): merge reviewed target source with release dev)
- refresh local export and release provenance for combined target source. (cda504b9a546 fix(release): refresh combined source portable artifacts)
- bind local release metadata to the committed combined-source artifact ancestry. (d4bd4938fa43 fix(release): project committed combined source provenance)

## Security

- refused Windows 8.3 aliases at the disposable distribution fixture boundary. (64979977922a fix(distribution): refuse Windows short-name aliases)
- bound locally accepted GitHub checks to exact workflow-run provenance without overstating server enforcement. (cb05b135eb0d fix(provider): bind exact workflow run provenance)
- independently qualified exact-name enforcement for Windows fixture paths. (6cb0a9ac8856 audit(distribution): accept Windows alias repair)
- Reject Windows 8.3 aliases and other unsafe fixture paths before destination mutation. (bb689227c6a6 fix(distribution): integrate portability hardening)
- Integrate reviewed Windows short-name alias refusal into the dev line. (cc85be9c472a docs(distribution): record portability integration)
- Preserve checksum, forbidden-path, and no-publish validation on regenerated archives. (da1051793d4c build(distribution): refresh portable artifacts)
- Record release metadata integrity defects before artifact integration. (4c0da8974daa audit(release): record artifact metadata findings)
- Preserve fail-closed target qualification review findings before integration. (b8fb89b917c9 audit(github): record workflow identity finding)
- portable pack provenance no longer trusts Git replacement refs. (b4d949c1ac1f fix(export): ignore Git replacement objects)

## Docs

- refresh source-bound local changelog and release-note previews. (671faa232216 docs(release): bind previews to repair source)
- bind release summaries to the converged generator source. (566a2c3b8b7d docs(release): refresh converged source previews)
- bind release previews to the hardened metadata generator. (e2ec8925adf7 docs(release): bind hardened preview source)
- normalize task evidence formatting. (963dcc7d6ede docs(queue): normalize workflow repair evidence)
- bind release summaries to the replacement-safe source checkpoint. (7863891e581d docs(release): bind replacement-safe source)
- bind release summaries to the paired-preview fail-closed repair. (1397b703a9c1 docs(release): bind paired-preview repair source)
- bind the repaired release-integrity candidate and its exact qualification evidence for review. (853d1c7a8486 docs(release): freeze replacement review candidate)
- refresh preview-only release text for the combined source. (66ef462c2b1b docs(changelog): bind combined source previews)

## Tests

- added stale-preview, file-set, hash, size, and cross-checkout regressions. (7bb41079e11f fix(release): bind metadata to final artifacts)
- added positive projection and unrelated-change refusal coverage. (bb308e64f4f2 fix(release): accept complete preview projection)
- require validation to preserve all generated release bytes. (edcd591a268b fix(release): converge bundle validation bytes)
- added JSON/Markdown mismatch and malformed JSON cases. (6cbd104cb048 fix(release): bind both preview representations)
- add official-shape and adversarial selector coverage. (7e56ad751615 fix(workflow): bind documented path ref)
- cover source-change concealment through git replace. (b4d949c1ac1f fix(export): ignore Git replacement objects)

## Internal

- record the bounded scope correction and review handoff. (7e56ad751615 fix(workflow): bind documented path ref)
- record source-review acceptance for a bounded dev integration. (f77ecba28741 audit(queue): record fresh release candidate review)
- record local target source acceptance with retained qualification notes. (d81d953a7674 audit(queue): record fresh target source review)
- register a source-only integration task. (43c86ffb92e1 audit(queue): admit target source dev integration)
- register a local artifact refresh with no publication effect. (4deeed08be90 audit(queue): admit combined target pack refresh)
- record qualified local combined-source artifacts and consumer evidence. (9cc4bb068837 audit(queue): qualify combined target artifacts)
- close reviewed local source and artifact dev integration. (3bdeb220cb31 audit(queue): close release and target dev integration)

## Risks

- GitHub target-policy checkpoint requires changes before target mutation (9bba1cecaec8 audit(provider): record target-policy defects)

## Malformed Commits

- None.

## Release Caveat

- Preview only. No tags, GitHub Releases, branch mutation, or publishing were performed.
