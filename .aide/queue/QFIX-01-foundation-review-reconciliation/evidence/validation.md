# Validation

Interpreter used: `py -3` (Python 3.11 on Windows).

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

## Focused Validation During Implementation

| Command | Result | Notes |
| --- | --- | --- |
| `py -3 scripts/aide self-check` | PASS_WITH_WARNINGS | after source update, next recommended step changed away from stale Q09 to QFIX-01/QFIX-02 guidance. |
| `py -3 scripts/aide self-check --write-report` | PASS_WITH_WARNINGS | refreshed non-canonical `.aide/runs/self-check/latest.md`; current next step is QFIX-02 after QFIX-01 review. |
| `py -3 -m unittest discover -s core/harness/tests -t .` | PASS | 26 tests after adding self-check/profile reconciliation coverage. |

## Final Validation

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short` | PASS_WITH_CHANGES | QFIX-01 docs/evidence/status files intentionally modified before final commit. |
| `git diff --check` | PASS | CRLF normalization warnings only; no whitespace errors. |
| `py -3 scripts/aide validate` | PASS_WITH_WARNINGS | 148 info, 7 warnings, 0 errors; legacy review-gate warnings and generated manifest source fingerprint drift remain outside QFIX-01. |
| `py -3 scripts/aide doctor` | PASS_WITH_WARNINGS | next step now QFIX-02 after QFIX-01 review; no stale Q09 recommendation. |
| `py -3 scripts/aide self-check` | PASS_WITH_WARNINGS | next step now QFIX-02 after QFIX-01 review; report-first and non-mutating without `--write-report`. |
| `py -3 -m unittest discover -s core/harness/tests -t .` | PASS | 26 tests. |
| `py -3 -m unittest discover -s core/compat/tests -t .` | PASS | 5 tests. |
| `py -3 -m unittest discover -s core/gateway/tests -t .` | PASS | 9 tests. |
| `py -3 -m unittest discover -s core/providers/tests -t .` | PASS | 8 tests. |
| `py -3 .aide/scripts/aide_lite.py doctor` | PASS | Q09-Q20 report as passed; no hard readiness failures. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | token ledger near-budget warnings only. |
| `py -3 .aide/scripts/aide_lite.py selftest` | PASS | internal AIDE Lite smoke checks pass. |
| `py -3 .aide/scripts/aide_lite.py eval run` | PASS | 6 pass, 0 warn, 0 fail; no provider/model/network calls. |
| `py -3 .aide/scripts/aide_lite.py route explain` | PASS | advisory `local_strong`, quality gates PASS, no provider/model/network calls. |
| `py -3 .aide/scripts/aide_lite.py provider validate` | PASS | provider metadata validates; live provider/model/network calls disabled. |
| `py -3 -m unittest discover -s .aide/scripts/tests -t .` | EXPECTED_FAIL | hidden `.aide` start directory remains non-importable; QFIX-02 owns this. |
| Targeted broad `rg` secret scan | PASS_AFTER_INSPECTION | matches were policy words, regex definitions, fake test fixtures, and path names; no real credential value found. |
| Strict key-shaped `rg` secret scan | PASS | no matches for real-looking keys/private-key markers. |

## Known Validation Warnings

- Q00-Q03, Q05, and Q06 retain legacy review-gate/raw-status warnings outside
  QFIX-01 scope.
- Generated managed-section manifest source fingerprint drift remains reported
  by Harness; this phase did not refresh generated contract artifacts.
- `.aide/scripts/tests` normal discovery remains intentionally unfixed for
  QFIX-02.
- Token ledger warnings are near-budget warnings only, not hard failures.
