# AIDE Release Notes Preview

This is a deterministic preview only. It does not publish a release.

source_range: 36d388a72b6e6e941ca84c93387d742f85af3064..5f9bb31a7a84255befb74b7a3841d09a045d1646
source_head: 5f9bb31a7a84255befb74b7a3841d09a045d1646
preview_only: true

## Highlights

- Fixed: Prevent unavailable changed-path observations from appearing unchanged. (498eb2c09e92)
- Fixed: Preserve uncertainty and known paths in test-impact planning. (5f9bb31a7a84)

## Validation Summary

- 498eb2c09e92: PASS: original missing-base defect observed without writes.
- 45f29220a30d: Attempt1: 12/13 passed, all seven new regressions passed; original failure retained.
- 5f9bb31a7a84: PASS: source13, ownership6 and delivered13; zero errors or skips.

## Known Risks

- 498eb2c09e92: Path mappings remain heuristic; T2 does not prove coverage or authorize tests.
- 45f29220a30d: The repaired selftest remains unqualified until its actual run.
- 5f9bb31a7a84: Heuristic advice is not complete dependency proof or execution authority.

## Follow-up

- 498eb2c09e92: Run the exact source job, retain evidence, then qualify the delivered payload.
- 45f29220a30d: Run allocation2 after exact review and fresh admission; retain all outcomes.
- 5f9bb31a7a84: Qualify the fixed source-range preview, independently review closure and integrate.

## Warnings

- None.

## Preview Caveat

- This draft is not an official release note and does not create tags or GitHub Releases.
