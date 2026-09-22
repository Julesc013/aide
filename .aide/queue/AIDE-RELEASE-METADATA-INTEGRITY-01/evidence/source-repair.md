# Source Repair Evidence

- Date: 2026-09-22
- Candidate state: pre-commit source repair
- Publication effect: none

## Repaired Invariants

- Release repository identity is read from the validated export manifest.
- Bundle identity is derived from the exported source commit.
- Checksums require exact coverage and exact `SHA256SUMS.txt` content.
- The asset index binds every eligible final file to its SHA-256 and byte size.
- Asset-index and validation files are excluded from self-referential sets.
- Stale or missing source previews are blocked from publication candidates.

## Validation

- `test_q31_export_pack_governance.py`: 6 passed.
- `test_export_import.py`: 25 passed.
- `test_q47_release_bundle.py`: 14 passed.
- `test_q48_github_release_draft.py`: 10 passed.
- Total: 55 passed, 0 failed, 0 skipped.
- `py_compile` and `git diff --check`: passed.
- Canonical `validate` and `doctor`: expected pre-regeneration failure because
  the retained Q47 asset/checksum files still encode the defect this source
  checkpoint repairs. No unrelated validation failure was reported.

## Remaining

- Commit and publish the source checkpoint.
- Generate and commit previews bound to that checkpoint.
- Regenerate the clean export/release candidate and validate final bytes.
- Obtain independent exact-commit rereview before `dev` integration.
