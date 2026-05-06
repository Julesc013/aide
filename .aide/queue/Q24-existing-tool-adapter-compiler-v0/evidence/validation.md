# Validation

Interpreter used: `py -3` on Windows.

## Baseline Before Q24 Edits

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short` | WARN | Worktree had pre-existing generated export-pack drift in `manifest.yaml` and `checksums.json`. |
| `git branch --show-current` | PASS | `main`. |
| `git rev-parse HEAD` | PASS | `4817b08319d10bef409debe802f9fff9b198526c`. |
| `git check-ignore .aide.local/` | PASS | `.aide.local/` ignored. |
| `py -3 scripts/aide validate` | PASS_WITH_WARNINGS | 148 info, 7 warnings; generated manifest drift and older review gates remain reported. |
| `py -3 scripts/aide doctor` | PASS_WITH_WARNINGS | Same warning posture; next-step guidance still points to QFIX-02 review. |
| `py -3 scripts/aide self-check` | PASS_WITH_WARNINGS | Report-only, no mutation, no external calls. |
| `py -3 .aide/scripts/aide_lite.py doctor` | PASS | Q09-Q20 present; adapter status current. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | Token ledger near-budget warnings only. |
| `py -3 .aide/scripts/aide_lite.py test` | PASS | Canonical AIDE Lite internal checks. |
| `py -3 .aide/scripts/aide_lite.py selftest` | PASS | Compatibility alias. |
| `py -3 -m unittest discover -s core/harness/tests -t .` | PASS | 27 tests. |
| `py -3 -m unittest discover -s core/compat/tests -t .` | PASS | 5 tests. |
| `py -3 -m unittest discover -s core/gateway/tests -t .` | PASS | 9 tests. |
| `py -3 -m unittest discover -s core/providers/tests -t .` | PASS | 8 tests. |
| `py -3 -m unittest discover -s .aide/scripts/tests` | PASS | 102 tests. |
| `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0` | PASS | 111 included files, 115 checksums, boundary PASS. |

## Final Validation

To be updated before review.
