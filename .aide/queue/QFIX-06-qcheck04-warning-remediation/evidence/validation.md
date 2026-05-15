# Validation

## Results

| Command | Result | Notes |
|---|---:|---|
| `py -3 scripts/aide compile --dry-run` | PASS | Confirmed only `.aide/generated/manifest.yaml` needed replacement before write. Reran after QFIX queue index updates. |
| `py -3 scripts/aide compile --write` | PASS | Refreshed generated manifest. |
| `py -3 scripts/aide validate` | PASS | 149 info, 0 warning, 0 error. |
| `py -3 scripts/aide doctor` | PASS | 149 info, 0 warning, 0 error. |
| `py -3 scripts/aide self-check` | PASS_WITH_NOTES | Validation passed; Q36-Q48, QCHECK, and QFIX review gates remain `needs_review` by policy. |
| `py -3 .aide/scripts/aide_lite.py selftest` | PASS | Completed in about 15.6 seconds after fixture trimming. |
| `py -3 .aide/scripts/aide_lite.py test` | PASS | Completed in about 16.7 seconds. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | Structural AIDE Lite validation passed. |
| `py -3 .aide/scripts/aide_lite.py doctor` | PASS | AIDE Lite doctor passed. |
| `py -3 .aide/scripts/aide_lite.py eval run` | PASS | 132 golden tasks passed, 0 warning, 0 fail. |
| `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0` | PASS | 629 included files, 632 checksum entries, boundary PASS. |
| `py -3 .aide/scripts/aide_lite.py pack-status` | PASS | Checksums valid, boundary PASS, provenance records dirty source. |
| `py -3 .aide/scripts/aide_lite.py release bundle` | PASS | Local-only release bundle regenerated; no publish/tag/upload. |
| `py -3 .aide/scripts/aide_lite.py release validate` | PASS | Fixture extraction and checksum validation passed. |
| `py -3 .aide/scripts/aide_lite.py release draft` | PASS | Local draft regenerated; suggested tag only. |
| `py -3 .aide/scripts/aide_lite.py release draft-validate` | PASS | Draft remains unpublished and no-upload. |
| `py -3 .aide/scripts/aide_lite.py install validate` | PASS | No-apply, no target mutation, no overwrite, no automatic migration. |
| `py -3 .aide/scripts/aide_lite.py repair validate` | PASS | No-apply, no target mutation, no overwrite/delete, no automatic migration. |
| `py -3 .aide/scripts/aide_lite.py upgrade validate` | PASS | No-apply, no target mutation, no overwrite/delete, no automatic migration. |
| `py -3 .aide/scripts/aide_lite.py rollback validate` | PASS | No-apply, no overwrite/delete/managed-section removal. |
| `py -3 .aide/scripts/aide_lite.py uninstall validate` | PASS | No blanket `.aide` deletion and no unsafe removal defaults. |
| `py -3 -m unittest discover -s .aide/scripts/tests` | PASS | 300 tests passed in 508.590 seconds. This remediates the prior timeout warning. |
| `py -3 -m unittest discover -s core/harness/tests -t .` | PASS | 27 tests passed. |
| `py -3 -m unittest discover -s core/compat/tests -t .` | PASS | 5 tests passed. |
| `py -3 -m unittest discover -s core/gateway/tests -t .` | PASS | 9 tests passed. |
| `py -3 -m unittest discover -s core/providers/tests -t .` | PASS | 8 tests passed. |
| Targeted secret/local-state scan with `rg` | PASS_AFTER_INSPECTION | Full scan matches and 277 changed-file matches were policy, test, path, regex, changelog, or generated evidence references. No real secret, provider key, private key, `.env`, `.aide.local`, raw prompt, or raw response was found. |

## Fixture Performance Evidence

- Before trimming, `_write_minimal_repo()` materialized about 1261 files and `run_context()` on the fixture took about 5.0 seconds.
- After trimming, `_write_minimal_repo()` materialized about 361 files and `run_context()` on the fixture took about 1.1 seconds.
- The full `.aide/scripts/tests` discovery now completes successfully instead of timing out.

## Validation Notes

- `git diff --check` exited 0. Git reported CRLF normalization warnings for four touched test files and their export-pack copies; the actual source diffs are one-line test helper changes.
- `pack-status` reports `DIRTY_SOURCE_RECORDED` because export/release artifacts were intentionally regenerated before this remediation commit.
- Q36-Q48 and checkpoint/fix-forward packets remain review-gated; this task does not mark them passed.
