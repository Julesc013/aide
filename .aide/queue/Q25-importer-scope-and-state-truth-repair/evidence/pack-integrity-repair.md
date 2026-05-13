# Pack Integrity Repair

## Root Cause

`pack-status` validated `manifest.yaml` as a checksummed payload file. The
manifest is pack metadata containing source commit and dirty-state provenance,
so it changes as the pack is regenerated. Treating it as payload made the
committed pack vulnerable to predictable metadata drift and caused the latest
checkpoint to see a `manifest.yaml` checksum mismatch.

## Old Behavior

- `checksums.json` listed `manifest.yaml`.
- `pack-status` failed when the committed manifest differed from the checksum
  entry.
- Export regeneration could make `pack-status` pass locally, but the convention
  was fragile because mutable metadata and payload were not separated.

## New Behavior

- `checksums.json` now uses schema
  `q25.aide-lite-pack-checksums.v1`.
- Checksum scope is `payload-and-static-pack-docs`.
- Excluded metadata files are:
  - `manifest.yaml`
  - `checksums.json`
  - `export-report.md`
- `validate_pack_checksums` now fails if an excluded metadata file appears in
  the checksum map.
- `validate_pack_checksums` now fails if a non-metadata payload file exists in
  the pack but is missing from `checksums.json`.
- Payload tampering still fails validation; tests modify
  `files/.aide/scripts/aide_lite.py` and confirm a checksum mismatch.
- The Q18 local-state example file
  `.aide.local.example/secrets/README.md` is tracked through a narrow
  `.gitignore` exception and exported as a safe documentation-only example;
  real `secrets/**` roots remain ignored and forbidden.
- `pack-status` prints up to five checksum problem details when validation
  fails.

## Provenance Rule

`manifest.yaml` records:

- `source_commit`
- `source_dirty_state`
- generator id/version
- no raw prompt/response storage
- no provider/model calls

If the source tree is dirty when `export-pack` runs, `source_dirty_state: true`
is recorded. Q25 evidence notes that final regenerated pack artifacts were
produced during the Q25 repair worktree, so dirty provenance is truthful rather
than hidden.

## Validation Result

- `C:\Program Files\Hybrid\64bit\Vapoursynth\python.exe .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0`:
  PASS, 123 included files, 126 checksummed payload/static files.
- `C:\Program Files\Hybrid\64bit\Vapoursynth\python.exe .aide/scripts/aide_lite.py pack-status`: PASS,
  `checksums_valid: true`, `checksum_problems: 0`,
  `boundary_result: PASS`.
- `.aide/scripts/tests/test_export_import.py`: PASS; checksum tests cover
  metadata exclusion, payload mismatch detection, and unchecksummed payload
  detection.
