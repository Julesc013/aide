# Release Bundle Audit

## Artifact List

| Artifact | Size | SHA256 |
|---|---:|---|
| `.aide/release/dist/aide-lite-pack-v0.zip` | 747422 | `8fb17229ac54d9355170a28b6e4bce3182cf6ad1078d4e30c81f7d5ea461d660` |
| `.aide/release/dist/aide-lite-pack-v0.tar.gz` | 493045 | `a92d468eaedba29abb79557851ed3fe5226c6bcfda2a522ed9fb13d2548e93d7` |
| `.aide/release/dist/aide-lite-pack-v0.checksums.json` | present | `8498cee9dd0ae28eb5d37b22bf8c2fd79963a14274893e55991696d16b177824` |
| `.aide/release/dist/SHA256SUMS.txt` | present | `2c0b0537c4c03e0cc6e82653a16a076bbc9fe70540a62b51e967fa0a1edc0dcb` |
| `.aide/release/dist/manifest.yaml` | present | `0cc9793f69c9099f11bceb8f3d144d5cddc0d61bb25d99036420ecb0a4803065` |
| `.aide/release/dist/install.md` | present | `0c3798a4e10ed6f083f4d1b9fcd7c75ea0e54a66bef3e995a2ea0e564fbe244d` |

## Checksum Validation

`release checksums`: PASS.

`release validate`: PASS.

## Archive Contents Summary

Both archives extract with stable root `aide-lite-pack-v0/` and include:

- `manifest.yaml`
- `checksums.json`
- `import-policy.yaml`
- `install.md`
- `export-report.md`
- `files/.aide/scripts/aide_lite.py`

Each archive contained 634 entries during the audit.

## Forbidden Path Scan

No forbidden path was found inside the zip or tarball:

- `.git/`
- `.aide.local/`
- `.env`
- `secrets/`
- raw prompt/response logs
- provider keys

## Extraction Result

Zip extraction: PASS.

Tar extraction: PASS.

## Install Notes Summary

Install notes are present and correctly frame install/upgrade/repair/rollback/uninstall as observe/plan/dry-run flows unless a later apply phase authorizes mutation.

## Provenance Summary

Release provenance is present and marks the bundle local-only/no-publish. It records source branch `main`, source commit `1dacef0b00ef02ee8e8e605d60c943334f4f962c`, and dirty state true.
