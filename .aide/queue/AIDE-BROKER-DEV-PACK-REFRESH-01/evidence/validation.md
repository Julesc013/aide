# Validation

- Broad intent compilation passed but classified the unsplit release-shaped
  request as blocked. This task admits only local non-publishing generation and
  validation under the existing Q47 boundary.
- `export-pack`: PASS; 826 files, 829 checksums, boundary PASS.
- `pack-status`: PASS; checksums, provenance, and boundary have zero problems.
- `release bundle`: PASS; bundle `aide-lite-pack-v0-b3e5c7aa2a1732fa`,
  11 artifacts, no-publish, no tag, no upload, no GitHub release.
- `release validate`, `release status`, and `release checksums`: PASS.
- `release draft` and `release draft-validate`: PASS; 12 checksum-bound assets,
  preview-only local draft, no network API call.
- `release draft-status`, `upload-plan`, `checklist`, and
  `publication-boundary`: PASS; zero blockers and seven retained manual review
  items, with all publication effects false.
- `test_export_import.py`: 25 passed in 250.178 seconds.
- `test_q47_release_bundle.py`: 10 passed in 16.883 seconds.
- Canonical `validate`: PASS, including export provenance and release draft
  asset checksum checks.
- `doctor`: PASS.
- Generated path allowlist check: 26 paths, zero outside authorized export and
  release roots.
