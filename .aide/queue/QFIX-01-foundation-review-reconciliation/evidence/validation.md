# Validation

Baseline commands were run before edits. Final validation will be appended after
reconciliation work completes.

## Baseline Before Edits

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short` | PASS | clean |
| `git branch --show-current` | PASS | `main` |
| `git rev-parse HEAD` | PASS | `765571932b311f1f9b5310aeee5b2fa7aa55926d` |
| `py -3 scripts/aide validate` | PASS_WITH_WARNINGS | 148 info, 7 warnings, 0 errors; legacy review gates and generated manifest drift. |
| `py -3 scripts/aide doctor` | PASS_WITH_WARNINGS | stale next step still pointed to Q09. |
| `py -3 scripts/aide self-check` | PASS_WITH_WARNINGS | stale next step still pointed to Q09. |
| `py -3 .aide/scripts/aide_lite.py doctor` | PASS | Q09-Q20 artifacts present. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | token near-budget warnings only. |
| `py -3 .aide/scripts/aide_lite.py verify` | PASS | 89 checked files, 0 warnings, 0 errors. |
| `py -3 .aide/scripts/aide_lite.py eval run` | PASS | 6 pass, 0 warn, 0 fail. |
| `py -3 .aide/scripts/aide_lite.py route explain` | PASS | advisory route, quality gates PASS. |
| `py -3 .aide/scripts/aide_lite.py cache status` | PASS | `.aide.local/` ignored, no tracked local state. |
| `py -3 .aide/scripts/aide_lite.py provider validate` | PASS | provider metadata validates; live calls disabled. |
| `py -3 -m unittest discover -s core/harness/tests -t .` | PASS | 24 tests. |
| `py -3 -m unittest discover -s core/compat/tests -t .` | PASS | 5 tests. |
| `py -3 -m unittest discover -s core/gateway/tests -t .` | PASS | 9 tests. |
| `py -3 -m unittest discover -s core/providers/tests -t .` | PASS | 8 tests. |
| `py -3 -m unittest discover -s .aide/scripts/tests -t .` | EXPECTED_FAIL | hidden `.aide` start directory is not importable; QFIX-02 owns this. |
