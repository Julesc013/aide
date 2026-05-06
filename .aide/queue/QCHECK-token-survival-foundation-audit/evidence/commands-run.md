# Commands Run

Working directory for all commands: `D:\Projects\AIDE\aide`.

Interpreter: `py -3` / Python 3.11.9.

## Git And Inventory

| Command | Result | Exit | Summary |
| --- | --- | ---: | --- |
| `git status --short` | PASS | 0 | Clean at audit start. |
| `git branch --show-current` | PASS | 0 | `main`. |
| `git rev-parse HEAD` | PASS | 0 | `84b579ce8e50a38aecad23cd6a7408e3646bd8c9`. |
| `git log --oneline -20` | PASS | 0 | Q20 commits visible at head. |
| Python deterministic max-depth-3 inventory | PASS | 0 | 417 files listed excluding `.git`. |
| `git status --ignored --short .aide.local .aide.local/; git check-ignore .aide.local/` | PASS | 0 | `.aide.local/` is ignored. |
| `git ls-files` count | PASS | 0 | 804 tracked files. |
| `git ls-files .aide.local .aide.local/ .env secrets` | PASS | 0 | no tracked local-state/secret paths. |

## Harness

| Command | Result | Exit | Summary |
| --- | --- | ---: | --- |
| `py -3 scripts/aide validate` | PASS_WITH_WARNINGS | 0 | 148 info, 7 warnings, 0 errors; warnings are older review gates and generated manifest drift. |
| `py -3 scripts/aide doctor` | PASS_WITH_WARNINGS | 0 | same structural posture; no hard errors. |
| `py -3 scripts/aide self-check` | PASS_WITH_WARNINGS | 0 | report-only, no external/model/provider/network calls; stale next step still points to Q09. |

## AIDE Lite

| Command | Result | Exit | Summary |
| --- | --- | ---: | --- |
| `py -3 .aide/scripts/aide_lite.py doctor` | PASS | 0 | Q09-Q20 artifacts present. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | 0 | token near-budget warnings for cache report and Q17/Q18 evidence only. |
| `py -3 .aide/scripts/aide_lite.py snapshot` | PASS | 0 | wrote snapshot, 791 files, no inline contents. |
| `py -3 .aide/scripts/aide_lite.py index` | PASS | 0 | wrote repo map/context index, 703 test mappings. |
| `py -3 .aide/scripts/aide_lite.py context` | PASS | 0 | latest context packet 1,926 chars / 482 tokens. |
| `py -3 .aide/scripts/aide_lite.py verify` | PASS | 0 | 89 checked files, 5 changed generated files, 0 warnings/errors. |
| `py -3 .aide/scripts/aide_lite.py review-pack` | PASS | 0 | latest review packet 6,520 chars / 1,630 tokens. |
| `py -3 .aide/scripts/aide_lite.py ledger scan` | PASS | 0 | 73 records, 3 budget warnings, 0 regressions. |
| `py -3 .aide/scripts/aide_lite.py ledger report` | PASS | 0 | records and summary rendered. |
| `py -3 .aide/scripts/aide_lite.py eval list` | PASS | 0 | 6 golden tasks. |
| `py -3 .aide/scripts/aide_lite.py eval run` | PASS | 0 | 6 pass / 0 warn / 0 fail. |
| `py -3 .aide/scripts/aide_lite.py eval report` | PASS | 0 | latest report PASS. |
| `py -3 .aide/scripts/aide_lite.py outcome report` | WARN | 0 | one advisory `packet_too_large` warning; no failures. |
| `py -3 .aide/scripts/aide_lite.py optimize suggest` | PASS | 0 | one advisory recommendation, no automatic mutation. |
| `py -3 .aide/scripts/aide_lite.py route list` | PASS | 0 | route classes and hard floors listed. |
| `py -3 .aide/scripts/aide_lite.py route validate` | PASS | 0 | route artifacts valid. |
| `py -3 .aide/scripts/aide_lite.py route explain` | PASS | 0 | route `local_strong`, quality gates PASS, advisory only. |
| `py -3 .aide/scripts/aide_lite.py cache status` | PASS | 0 | `.aide.local/` ignored, no tracked local state. |
| `py -3 .aide/scripts/aide_lite.py cache report` | PASS | 0 | 8 metadata keys, raw prompt/response false. |
| `py -3 .aide/scripts/aide_lite.py gateway status` | PASS | 0 | local/report-only status, no provider/model/network calls. |
| `py -3 .aide/scripts/aide_lite.py gateway endpoints` | PASS | 0 | health/status/route/summaries/version listed; forwarding forbidden. |
| `py -3 .aide/scripts/aide_lite.py gateway smoke` | PASS | 0 | endpoints returned safe local responses. |
| `py -3 .aide/scripts/aide_lite.py provider list` | PASS | 0 | 13 provider families, live calls disabled. |
| `py -3 .aide/scripts/aide_lite.py provider status` | PASS | 0 | provider status PASS, credentials false, forwarding false. |
| `py -3 .aide/scripts/aide_lite.py provider validate` | PASS | 0 | provider metadata validates, no obvious secrets. |
| `py -3 .aide/scripts/aide_lite.py provider contract` | PASS | 0 | no-call contract summary printed. |
| `py -3 .aide/scripts/aide_lite.py provider probe --offline` | PASS | 0 | offline metadata probe only. |
| `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md` | PASS | 0 | 3,654 chars / 914 tokens / within budget. |
| `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-review-packet.md` | PASS | 0 | 6,520 chars / 1,630 tokens / within budget. |
| `py -3 .aide/scripts/aide_lite.py selftest` | PASS | 0 | all internal checks pass. |

## Tests

| Command | Result | Exit | Summary |
| --- | --- | ---: | --- |
| `py -3 -m unittest discover -s core/harness/tests -t .` | PASS | 0 | 24 tests. |
| `py -3 -m unittest discover -s core/compat/tests -t .` | PASS | 0 | 5 tests. |
| `py -3 -m unittest discover -s .aide/scripts/tests -t .` | FAIL | 1 | `ImportError: Start directory is not importable`; existing hidden `.aide` discovery issue. |
| `py -3 -m unittest discover -s core/gateway/tests -t .` | PASS | 0 | 9 tests. |
| `py -3 -m unittest discover -s core/providers/tests -t .` | PASS | 0 | 8 tests. |
| direct `.aide/scripts/tests/test_*.py` execution | PASS | 0 | 90 tests across 10 test files. |

## Syntax, Diff, Secret, Local-State Checks

| Command | Result | Exit | Summary |
| --- | --- | ---: | --- |
| Python `py_compile` over `core`, `shared`, `.aide/scripts`, and `scripts/aide` | PASS | 0 | 55 compiled, 0 failed. |
| `git diff --check` | PASS | 0 | no whitespace errors; Windows line-ending warnings only. |
| broad targeted `rg` secret scan | PASS_AFTER_INSPECTION | 0 | matches are policy/test/template strings and paths, not actual secrets. |
| stricter raw prompt/key scan | PASS_AFTER_INSPECTION | 0 | matches are tests/policies asserting absence of raw prompt/response fields. |
| attempted strict `rg` key-shaped scan | FAIL | 1 | PowerShell quoting/parser error before scanning; replaced with a Python stdlib strict scan. |
| Python strict key-shaped secret scan | PASS | 0 | `STRICT_SECRET_MATCHES=0`. |
| `Test-Path .aide.local`, `.env`, `secrets` | PASS | 0 | all false. |

## Notes

- Several approved report commands refreshed non-canonical generated artifacts.
- No provider calls, model calls, outbound network calls, raw prompt logs, raw
  response logs, credentials, or `.aide.local/` state were produced.
