# Implementation Validation

## Baseline

- Executable archive regression: **FAIL as expected** for ZIP and tar.gz.
- Failure: filtered `files/.aide.local.example/secrets/README.md` remained in
  each archive's copied checksum register.

## Implemented Behavior

- Build a temporary release projection from permitted source-pack files.
- Regenerate the projected `manifest.yaml`, `checksums.json`, and
  `export-report.md` from actual projected bytes.
- Reject invalid projected checksums, forbidden paths, or export-boundary
  violations before archive creation.
- Validate each extracted archive's checksums and exact manifest/payload set.
- Document isolated import commands that execute the delivered CLI.

## Automated Results

- `test_q47_release_bundle.py`: **PASS**, 9 tests.
- `test_export_import.py`: **PASS**, 15 tests.
- `test_q31_export_pack_governance.py`: **PASS**, 6 tests.
- `test_q48_github_release_draft.py`: **PASS**, 8 tests.
- `test_aide_self_consumer_fixture_v0.py`: **PASS**, 7 tests.
- `test_aide_distribution_product_status_projection.py`: **PASS**, 1 test.
- Total recorded tests: **46 passed, 0 failed, 0 skipped**.

## Dirty-Source Preview Canary

- Export pack: 826 payload files, 829 checksum entries, boundary PASS.
- Release validation: PASS for ZIP and tar.gz; no publication effects.
- Fresh disposable Git target: dry-run PASS, safe import PASS.
- Safe import: 814 writes, 0 conflicts, 16 intentional broad-root skips.
- Installed target CLI `doctor`: PASS with expected missing-generated-state warnings.
- Repeated ZIP and tar.gz generation: byte-identical.

The preview artifacts were restored after this check. Final tracked artifacts
must be regenerated from the clean implementation commit so their source
identity does not claim this dirty pre-commit state as the release candidate.
