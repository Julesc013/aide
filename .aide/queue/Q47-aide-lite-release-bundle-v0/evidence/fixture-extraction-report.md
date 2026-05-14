# Fixture Extraction Report

## Result

- `py -3 .aide/scripts/aide_lite.py release validate`: PASS.
- Fixture extraction result: PASS.
- Checksum validation result: PASS.
- Forbidden path scan result: PASS.

## Archive Fixtures

| Archive | Root Present | Required Files | Forbidden Paths | Problems | Result |
| --- | --- | --- | --- | --- | --- |
| `.aide/release/dist/aide-lite-pack-v0.zip` | true | 6/6 | 0 | 0 | PASS |
| `.aide/release/dist/aide-lite-pack-v0.tar.gz` | true | 6/6 | 0 | 0 | PASS |

## Required Files Verified

- `manifest.yaml`
- `checksums.json`
- `import-policy.yaml`
- `install.md`
- `export-report.md`
- `files/.aide/scripts/aide_lite.py`

## Forbidden Paths

The archive validator checks for `.git/`, `.aide.local/`, `.env`, `secrets/`,
raw prompt logs, and raw response logs. Both archives passed with zero hits.

## No Apply

Fixture validation extracts and inspects archives only. It does not install AIDE,
apply install/repair/upgrade/rollback/uninstall operations, mutate target repos,
or run provider/model/network calls.
