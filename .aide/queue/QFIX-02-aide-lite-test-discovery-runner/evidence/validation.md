# Validation

Interpreter used: `py -3` (Python 3.11 on Windows).

## Baseline Before Edits

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short` | PASS | clean |
| `git branch --show-current` | PASS | `main` |
| `git rev-parse HEAD` | PASS | `9adcfb0ca18a214d9955818839926185256d6392` |
| `py -3 scripts/aide validate` | PASS_WITH_WARNINGS | 148 info, 7 warnings, 0 errors; legacy review gates and generated manifest drift. |
| `py -3 scripts/aide doctor` | PASS_WITH_WARNINGS | next step points to QFIX-02 after QFIX-01 review. |
| `py -3 scripts/aide self-check` | PASS_WITH_WARNINGS | report-only; Q09-Q20 accepted with notes; QFIX-02 next. |
| `py -3 .aide/scripts/aide_lite.py doctor` | PASS | Q09-Q20 artifacts present and passed. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | token near-budget warnings only. |
| `py -3 .aide/scripts/aide_lite.py selftest` | PASS | internal AIDE Lite smoke checks pass. |
| `py -3 -m unittest discover -s .aide/scripts/tests -t .` | FAIL | start directory is not importable under repo-root top-level discovery. |
| `py -3 -m unittest discover -s .aide/scripts/tests` | PASS | 90 tests pass; no top-level package import constraint. |
| `py -3 -m unittest discover -s core/harness/tests -t .` | PASS | 26 tests. |
| `py -3 -m unittest discover -s core/compat/tests -t .` | PASS | 5 tests. |
| `py -3 -m unittest discover -s core/gateway/tests -t .` | PASS | 9 tests. |
| `py -3 -m unittest discover -s core/providers/tests -t .` | PASS | 8 tests. |

Final validation will be appended after the test runner repair.
