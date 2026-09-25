# AIDE Release Notes Preview

This is a deterministic preview only. It does not publish a release.

source_range: HEAD latest 50 commits
source_head: 7624d9f4b54207a33ad3ed0ba434143a1fda9398
preview_only: true

## Highlights

- Added: exact historical message dispositions to the dev source ancestry. (e40aec47dd2d)
- Added: restore a missing receipt-owned file from the exact delivered pack. (49f38d12f425)
- Added: receipt-backed read-only removal planning in the delivered portable CLI. (1a25e33effc5)
- Fixed: allow accountable AEST historical decisions while retaining strict raw policy results. (7a2305f51894)
- Fixed: prevent dirty-source provenance in the local combined artifact projection. (1fa02a8594fe)

## Validation Summary

- 10fc01a6a827: PASS: 29 import, 18 release, 11 draft, and 6 governance tests against final source.
- 8cad56c0a612: PASS: first postcommit generator cycle changed 18 expected files.
- 1c0327782f8a: PASS: 29 import, 18 release, 11 draft, and 6 governance tests on final source.
- 71416928aa36: PASS: SHA-256 of external original and working copy match.
- a5cd5ca5ddf7: PASS: accepted commit and tree identities, candidate ancestry, and final ZIP and tar.gz hashes.
- 7a2305f51894: PASS: 23 focused commit-recovery tests and canonical validate and doctor.
- e40aec47dd2d: PASS: read-only merge preflight, 23 focused historical tests, exact accepted and raw range checks, and staged diff checks.
- 3326868b534d: PASS: 23 historical, 29 import, 18 release, 11 draft, and 6 portable governance tests.
- 1fa02a8594fe: PASS: pack-status records clean source provenance; release and draft validation pass.
- 8933792f37c5: PASS: pack provenance is PASS_SOURCE_ANCESTOR; release and draft validation both pass.

## Known Risks

- 10fc01a6a827: Post-commit ancestry projection and human dev review remain open; no publication occurred.
- 8cad56c0a612: Stable publication and human dev review remain separate gates.
- 1c0327782f8a: Dev integration, complete lifecycle apply, native/hosted qualification, and stable release remain open.
- 71416928aa36: The external original is required for byte-exact original verification.
- a5cd5ca5ddf7: Post-integration replay and final lifecycle qualification remain open.
- 7a2305f51894: This does not qualify product behavior, native or hosted effects, or release publication.
- e40aec47dd2d: This source merge is not a qualified delivered artifact or release candidate until generated outputs and combined tests pass.
- 3326868b534d: Post-commit replay and independent integration review remain open; no release is published.
- 1fa02a8594fe: This remains a local preview; post-commit ancestry and independent integration review still need confirmation.
- 8933792f37c5: Independent integration review, remote dev integration, and full release qualification remain open.

## Follow-up

- 10fc01a6a827: Project committed artifact ancestry, verify clean replay, and record the exact review subject.
- 8cad56c0a612: Replay from committed clean tree and preserve the exact final review packet.
- 1c0327782f8a: Obtain exact human review of the frozen source/artifact subject before dev integration.
- 71416928aa36: Use the frozen `8cad56c0` subject for human dev-integration review.
- a5cd5ca5ddf7: Publish the clean task branch, fast-forward dev if the remote base remains unchanged, then verify provenance and remote identity.
- 7a2305f51894: Integrate eligible source and decisions against current dev, regenerate derived outputs, and verify combined validation.
- e40aec47dd2d: Regenerate through the current generator, validate combined source and archives, obtain independent integration review, then update remote dev.
- 3326868b534d: Verify committed artifact provenance and replay, obtain exact integration review, then fast-forward qualified source to dev.
- 1fa02a8594fe: Check the committed pack as a source ancestor, verify byte-stable replay and extracted consumer, then obtain exact integration review.
- 8933792f37c5: Rerun validation after this commit, freeze the exact integration candidate, and request technical review.

## Warnings

- None.

## Preview Caveat

- This draft is not an official release note and does not create tags or GitHub Releases.
