# Validation

## Commands

| Command | Result | Notes |
|---|---:|---|
| `git status --short` | PASS | Clean at start of QFIX-07. |
| `py -3 .aide/scripts/aide_lite.py task status` | PASS | No failed or blocked tasks found; remaining non-passed tasks are implemented `needs_review` gates. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id QFIX-06-qcheck04-warning-remediation` | PASS | Complete, missing evidence 0. |
| `py -3 scripts/aide self-check` | PASS_WITH_NOTES | Structural validation passed; implemented `needs_review` gates remain not accepted for dependency until review. |
| `py -3 scripts/aide compile --dry-run` | PASS | Manifest-only replacement after queue index update. |
| `py -3 scripts/aide compile --write` | PASS | Refreshed `.aide/generated/manifest.yaml`. |
| `git diff --check` | PASS | No whitespace errors. |
| `py -3 scripts/aide validate` | PASS | 149 info, 0 warning, 0 error. |
| `py -3 scripts/aide doctor` | PASS | 149 info, 0 warning, 0 error. |
| `py -3 scripts/aide self-check` | PASS_WITH_NOTES | Review gates remain by policy. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | AIDE Lite structural validation passed. |
| `py -3 .aide/scripts/aide_lite.py doctor` | PASS | AIDE Lite doctor passed. |
| `py -3 .aide/scripts/aide_lite.py test` | PASS | AIDE Lite internal test passed. |
| `py -3 .aide/scripts/aide_lite.py selftest` | PASS | AIDE Lite selftest passed. |
| `py -3 .aide/scripts/aide_lite.py pack-status` | PASS | Checksums valid, boundary PASS, provenance `DIRTY_SOURCE_RECORDED`. |
| `py -3 .aide/scripts/aide_lite.py release validate` | PASS | Local release validation passed; no publish/tag/upload. |
| `py -3 .aide/scripts/aide_lite.py release draft-validate` | PASS | Draft is local-only; no tag/release/upload/network. |
| `py -3 .aide/scripts/aide_lite.py install validate` | PASS | No-apply, no overwrite, no target mutation. |
| `py -3 .aide/scripts/aide_lite.py repair validate` | PASS | No-apply, no overwrite/delete, no target mutation. |
| `py -3 .aide/scripts/aide_lite.py upgrade validate` | PASS | No-apply, no overwrite/delete, no automatic migration. |
| `py -3 .aide/scripts/aide_lite.py rollback validate` | PASS | No-apply, no overwrite/delete/managed-section removal. |
| `py -3 .aide/scripts/aide_lite.py uninstall validate` | PASS | No blanket `.aide` deletion; no unsafe removal defaults. |
| `py -3 -m unittest discover -s .aide/scripts/tests` | PASS | 300 tests passed in 542.084 seconds. |
| `py -3 -m unittest discover -s core/harness/tests -t .` | PASS | 27 tests passed. |
| `py -3 -m unittest discover -s core/compat/tests -t .` | PASS | 5 tests passed. |
| `py -3 -m unittest discover -s core/gateway/tests -t .` | PASS | 9 tests passed. |
| `py -3 -m unittest discover -s core/providers/tests -t .` | PASS | 8 tests passed. |
| `py -3 .aide/scripts/aide_lite.py eval run` | PASS | 132 golden tasks passed, 0 warn, 0 fail. |
| `py -3 .aide/scripts/aide_lite.py changelog preview --limit 50` | PASS | Preview only; 15 malformed historical commits reported for review. |
| `py -3 .aide/scripts/aide_lite.py changelog validate` | PASS | Preview artifacts validate. |
| `py -3 .aide/scripts/aide_lite.py github advisory` | PASS | Advisory only; no GitHub API, network, workflow, or branch mutation. |
| `py -3 .aide/scripts/aide_lite.py github validate` | PASS | GitHub advisory artifacts validate. |
| Changed-file secret/local-state scan with `rg` | PASS_AFTER_INSPECTION | 32 matches, all generated changelog/eval/policy/test terms; no real secret, provider key, private key, `.env`, `.aide.local`, raw prompt, or raw response found. |

## Notes

- Fixture output inside raw unittest discovery intentionally shows `FIXTURE-TASK` as partial inside a temp fixture; it is not a repository queue item.
- Current AIDE-local implementation is validation-clean, but review-gated phases remain `needs_review` and are not self-approved.
