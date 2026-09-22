# Artifact Refresh Validation

## Identity

- Source commit: `c730eac442021cdd6f71e6d8038d096af0c6378b`.
- Bundle id: `aide-lite-pack-v0-c730eac442021cdd`.
- ZIP SHA-256: `3f24c8e27e21c1884c866ad4faf15538a1fd53cb2905e9d9abe41f6fbe170905`.
- tar.gz SHA-256: `fb855c0e88d26138014038ff3ed5c2c5f2fc26a57f08fafd0f842492a327e758`.
- Export payload: 826 included files and 829 checksums.
- Local release bundle: 11 artifacts.
- Preview draft: 12 checksum-bound assets.

## Results

- PASS: `export-pack` and `pack-status`; zero checksum, provenance, or boundary
  problems.
- PASS: `release bundle`, `release validate`, `release status`, and
  `release checksums`.
- PASS: the preview-only `release draft` after deterministic checksum rebind,
  followed by `release draft-validate`.
- PASS: 25 `test_export_import.py` consumer cases in 274.013 seconds.
- PASS: 10 `test_q47_release_bundle.py` cases in 17.076 seconds.
- PASS: canonical `validate`, `doctor`, and `git diff --check`.
- NOT RUN: tag creation, upload, GitHub Release publication, main promotion,
  hosted provider effects, and non-disposable target mutation.

All generated outputs remain local and explicitly no-publish. The first draft
validation observed the expected changed `release-validation.json` checksum;
rerunning the deterministic draft generator rebound that asset and passed.
After committing these generated files, provenance may classify the source as
an ancestor and require one final release-metadata rebind.

## Committed Provenance Closure

- Artifact commit: `da1051793d4c91ccff8d6c23b66ce1fa598729aa`.
- Post-commit pack provenance: `PASS_SOURCE_ANCESTOR` with zero checksum,
  provenance, or boundary problems.
- Post-commit bundle id: `aide-lite-pack-v0-da1051793d4c91cc`.
- The deterministic second pass changed twenty release metadata records and
  did not change the ZIP or tar.gz bytes.
- PASS: post-commit release validation and draft checksum validation.

Independent review and exact `dev` integration remain pending. Public release
effects remain prohibited by this task.
