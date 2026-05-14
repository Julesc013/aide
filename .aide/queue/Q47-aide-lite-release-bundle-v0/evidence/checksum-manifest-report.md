# Checksum And Manifest Report

## Checksum Validation

- `py -3 .aide/scripts/aide_lite.py release checksums`: PASS.
- `.aide/release/dist/aide-lite-pack-v0.checksums.json`: present and valid.
- `.aide/release/dist/SHA256SUMS.txt`: present and valid.
- `release validate`: recomputed artifact checksums and passed.

## Release Manifest

- Path: `.aide/release/dist/manifest.yaml`
- `release manifest`: PASS.
- Manifest is marked `no_publish: true`.
- Manifest references the archive assets, install notes, checksum file, provenance file, and validation file.

## Provenance

- Path: `.aide/release/dist/release-provenance.json`
- `release provenance`: PASS.
- Source commit: `e5a2692d3c4593aaf9931b15adb55a201e703ce0`
- Source branch: `main`
- Dirty state: true, recorded explicitly.
- Export pack manifest SHA256: `3eee245498fdea699b4accf8e60c5bd7b33f5f7b09a0797e8e4d033ce95d93ae`
- Export pack checksums SHA256: `3520a96f90814c89339abeaa899d04ab546480e92880ed80d490130038650dad`
- No-publish flag: true.

## Pack Status

- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS.
- Provenance result: `DIRTY_SOURCE_RECORDED`.
- Boundary result: PASS.
- Problems: 0.
