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

## Diagnosis Commands

| Command | Result | Notes |
| --- | --- | --- |
| `py -3 -m unittest .aide/scripts/tests/test_aide_lite.py` | FAIL_NON_CANONICAL | Direct dotted-module invocation through the hidden `.aide` path fails with `ValueError: Empty module name`; this is another invalid Python import form, not a failing AIDE Lite test. |
| `py -3 -m unittest discover -s .aide/scripts/tests` | PASS | Standard discovery without `-t .` loads the files directly and passes. |
| `py -3 -m unittest discover -s .aide/scripts/tests -t .` | FAIL_NON_CANONICAL | Preserved as the diagnosed old broken command; it requires `.aide/scripts/tests` to be importable from repo root, which is not a valid package path. |

## Final Review Validation

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short` | PASS | showed the intended QFIX-02 working set before the final docs/evidence commit. |
| `py -3 scripts/aide validate` | PASS_WITH_WARNINGS | 148 info, 7 warnings, 0 errors; warnings are legacy review-gate nuance and stale generated manifest source fingerprint. |
| `py -3 scripts/aide doctor` | PASS_WITH_WARNINGS | next recommended step is QFIX-02 review according to `status.yaml`. |
| `py -3 scripts/aide self-check` | PASS_WITH_WARNINGS | no stale Q09 guidance; QFIX-02 is in `needs_review`. |
| `py -3 .aide/scripts/aide_lite.py doctor` | PASS | after `adapt`, the AIDE Lite managed section status is current. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | token ledger near-budget warnings only. |
| `py -3 .aide/scripts/aide_lite.py adapt` | PASS | refreshed the managed AIDE Lite guidance section in `AGENTS.md` after the new `test` command wording changed. |
| `py -3 .aide/scripts/aide_lite.py test` | PASS | canonical AIDE Lite validation command. |
| `py -3 .aide/scripts/aide_lite.py selftest` | PASS | compatibility alias remains healthy. |
| `py -3 -m unittest discover -s .aide/scripts/tests -t .` | FAIL_NON_CANONICAL | expected and documented; do not use as canonical validation. |
| `py -3 -m unittest discover -s .aide/scripts/tests` | PASS | 94 AIDE Lite tests pass after QFIX-02. |
| `py -3 -m unittest discover -s core/harness/tests -t .` | PASS | 27 tests pass after the self-check guidance regression test was added. |
| `py -3 -m unittest discover -s core/compat/tests -t .` | PASS | 5 tests. |
| `py -3 -m unittest discover -s core/gateway/tests -t .` | PASS | 9 tests. |
| `py -3 -m unittest discover -s core/providers/tests -t .` | PASS | 8 tests. |
| `git diff --check` | PASS | only CRLF normalization warnings from Git for already-edited text files; no whitespace errors. |
| targeted secret scan with `rg` | PASS_AFTER_INSPECTION | matches were policy/example/test strings such as `secrets_policy`, `OPENAI_API_KEY`, and regex patterns; no real secrets, provider keys, raw prompts, or raw responses found. The optional root `tests` path is absent in this repo. |
| strict key-shaped scan with `rg` | PASS | no `sk-*`, `sk-ant`, or real provider-key shaped matches found; the optional root `tests` path is absent in this repo. |

## Known Non-Blocking Warnings

- `py -3 -m unittest discover -s .aide/scripts/tests -t .` remains intentionally non-canonical and failing for the hidden `.aide` path.
- Harness still reports older Q00-Q03/Q05/Q06 review-gate nuance and generated manifest source fingerprint drift.
- AIDE Lite validation still reports token ledger near-budget warnings.
- Q21 export/import has not been started.
