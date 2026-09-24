# AIDE Release Notes Preview

This is a deterministic preview only. It does not publish a release.

source_range: HEAD latest 50 commits
source_head: 2b4f5de885a59d561478759fa38b0f83a66312c7
preview_only: true

## Highlights

- Security: Reject Windows 8.3 aliases and other unsafe fixture paths before destination mutation. (bb689227c6a6)
- Security: Integrate reviewed Windows short-name alias refusal into the dev line. (cc85be9c472a)
- Security: Preserve checksum, forbidden-path, and no-publish validation on regenerated archives. (da1051793d4c)
- Security: Record release metadata integrity defects before artifact integration. (4c0da8974daa)
- Security: Preserve fail-closed target qualification review findings before integration. (b8fb89b917c9)
- Security: portable pack provenance no longer trusts Git replacement refs. (b4d949c1ac1f)
- Added: Admit deterministic release metadata integrity repair. (5ad6aa979971)
- Added: local customization explanation and opt-in import feedback. (98de5ee1531e)
- Changed: Begin commit-bound portable artifact refresh after portability integration. (c730eac44202)
- Changed: Refresh portable artifacts for the integrated Windows path-hardening source. (da1051793d4c)
- Changed: exact no-publish candidate assets and draft evidence regenerated. (8369ac540e4a)
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
- Fixed: dry-run recovery mutation and project-owned metadata payload boundary. (9b21e183d462)
- Fixed: Windows alias route into project-owned customization metadata. (2b4f5de885a5)
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

- bb689227c6a6: PASS: candidate range commit policy check for all six commits.
- cc85be9c472a: PASS: 118 of 126 focused tests, with eight symlink or FIFO capability skips and zero failures.
- c730eac44202: PASS: refresh worktree starts clean at dev cc85be9c472a16f39aae98ba00fd5de145098862.
- da1051793d4c: PASS: export pack with 826 files, 829 checksums, and zero provenance or boundary problems.
- da1051793d4c: PASS: export pack with 826 files, 829 checksums, and zero provenance or boundary problems.
- 38fe712810b8: PASS: pack provenance is PASS_SOURCE_ANCESTOR with zero checksum, provenance, or boundary problems.
- 4c0da8974daa: PASS: 43 relevant unit tests, canonical validate, doctor, commit-range policy, and diff checks.
- b8fb89b917c9: PASS: 134 of 135 affected tests with one Windows symlink-privilege skip and zero failures.
- 5ad6aa979971: PASS: exact failed candidate and review identities recorded.
- 7bb41079e11f: PASS: 55 adjacent export, import, Q47, and Q48 tests.

## Known Risks

- bb689227c6a6: Post-merge combined-tree tests and portable artifact provenance refresh remain required.
- cc85be9c472a: Portable export and release-bundle provenance remain stale until regenerated from clean landed dev.
- c730eac44202: Generated outputs are not yet refreshed and canonical validation remains red for known provenance drift.
- da1051793d4c: This generated-byte commit may require one deterministic post-commit provenance rebind.
- da1051793d4c: This generated-byte commit may require one deterministic post-commit provenance rebind.
- 38fe712810b8: The artifacts remain local no-publish outputs pending independent review and dev integration.
- 4c0da8974daa: The exact artifact-refresh candidate remains blocked from dev integration.
- b8fb89b917c9: GitHub target qualification remains fixture-only and blocked from hosted effects.
- 5ad6aa979971: The failed artifact candidate remains blocked until implementation and independent rereview pass.
- 7bb41079e11f: Generated release artifacts are not qualified until regenerated after the source-bound preview commit.

## Follow-up

- bb689227c6a6: Run the focused and adjacent suites on the merged tree, record exact evidence, and regenerate commit-bound portable artifacts.
- cc85be9c472a: Push the exact dev checkpoint, regenerate portable artifacts in a bounded refresh task, and validate extracted consumer bytes.
- c730eac44202: Generate export, bundle, and preview draft outputs from this clean checkpoint and validate extracted consumer artifacts.
- da1051793d4c: Revalidate committed provenance, close any second-order metadata changes, obtain exact review, and integrate the refresh into dev.
- da1051793d4c: Revalidate committed provenance, close any second-order metadata changes, obtain exact review, and integrate the refresh into dev.
- 38fe712810b8: Publish the exact candidate, obtain independent review, integrate it into dev, and rerun landed-tree validation.
- 4c0da8974daa: Admit a generator repair, add cross-checkout and asset-index regressions, regenerate all affected artifacts, and request exact rereview.
- b8fb89b917c9: Expand the task scope explicitly, parse and bind path-at-ref identity, add adversarial fixtures, and request exact rereview.
- 5ad6aa979971: Add failing regressions, repair the generator dependency graph, and regenerate exact local artifacts.
- 7bb41079e11f: Generate source-bound previews, regenerate clean artifacts, validate consumers, and obtain exact independent rereview.

## Warnings

- None.

## Preview Caveat

- This draft is not an official release note and does not create tags or GitHub Releases.
