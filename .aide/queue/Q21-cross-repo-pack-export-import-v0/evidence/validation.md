# Validation

Interpreter used: `py -3` (Python 3.11 on Windows).

## Baseline Before Edits

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short` | PASS | clean |
| `git branch --show-current` | PASS | `main` |
| `git rev-parse HEAD` | PASS | `997cfe5c52e0bc5e9075ab3bca417bd7ba231867` |
| `git check-ignore .aide.local/` | PASS | `.aide.local/` is ignored. |
| `py -3 scripts/aide validate` | PASS_WITH_WARNINGS | 148 info, 7 warnings, 0 errors; inherited review-gate and generated-manifest warnings. |
| `py -3 scripts/aide doctor` | PASS_WITH_WARNINGS | no hard structural errors; still recommends QFIX-02 review because QFIX-02 is at review gate. |
| `py -3 scripts/aide self-check` | PASS_WITH_WARNINGS | report-only; Q09-Q20 accepted with notes; QFIX-02 at review gate. |
| `py -3 .aide/scripts/aide_lite.py doctor` | PASS | Q09-Q20 artifacts present. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | token ledger near-budget warnings only. |
| `py -3 .aide/scripts/aide_lite.py selftest` | PASS | internal AIDE Lite checks pass. |
| `py -3 .aide/scripts/aide_lite.py test` | PASS | QFIX-02 canonical AIDE Lite validation command. |
| `py -3 -m unittest discover -s .aide/scripts/tests` | PASS | 94 tests. |
| `py -3 -m unittest discover -s core/harness/tests -t .` | PASS | 27 tests. |
| `py -3 -m unittest discover -s core/compat/tests -t .` | PASS | 5 tests. |
| `py -3 -m unittest discover -s core/gateway/tests -t .` | PASS | 9 tests. |
| `py -3 -m unittest discover -s core/providers/tests -t .` | PASS | 8 tests. |

Final validation will be appended after export/import implementation.
