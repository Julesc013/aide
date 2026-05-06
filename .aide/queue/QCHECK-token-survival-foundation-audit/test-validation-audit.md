# Test And Validation Audit

## Summary

| Area | Command | Result | Notes |
| --- | --- | --- | --- |
| Harness | `py -3 scripts/aide validate` | PASS_WITH_WARNINGS | 148 info, 7 warnings, 0 errors |
| Harness | `py -3 scripts/aide doctor` | PASS_WITH_WARNINGS | same structural warnings |
| Harness | `py -3 scripts/aide self-check` | PASS_WITH_WARNINGS | report-only; stale next step |
| AIDE Lite | `doctor` | PASS | Q09-Q20 artifacts present |
| AIDE Lite | `validate` | PASS | token near-budget warnings |
| AIDE Lite | `snapshot/index/context` | PASS | generated metadata only |
| AIDE Lite | `verify` | PASS | 0 warnings/errors before audit files |
| AIDE Lite | `review-pack` | PASS | 1,630-token review packet after audit run |
| AIDE Lite | `ledger scan/report` | PASS | 73 records; 3 near-budget warnings |
| AIDE Lite | `eval run/report` | PASS | 6 pass, 0 warn, 0 fail |
| AIDE Lite | `outcome report` | WARN | one packet-size advisory |
| AIDE Lite | `route validate/explain` | PASS | advisory local_strong route |
| AIDE Lite | `cache status/report` | PASS | `.aide.local/` ignored, 8 keys |
| AIDE Lite | `gateway status/endpoints/smoke` | PASS | local/report-only endpoints |
| AIDE Lite | `provider list/status/validate/contract/probe --offline` | PASS | 13 families; live calls false |
| AIDE Lite | `selftest` | PASS | includes provider checks |
| Harness tests | `core/harness/tests` | PASS | 24 tests |
| Compatibility tests | `core/compat/tests` | PASS | 5 tests |
| Gateway tests | `core/gateway/tests` | PASS | 9 tests |
| Provider tests | `core/providers/tests` | PASS | 8 tests |
| AIDE Lite tests | `.aide/scripts/tests` discover | FAIL | hidden start directory not importable |
| AIDE Lite tests | direct `test_*.py` execution | PASS | 90 tests |
| Syntax | py_compile key files | PASS | 55 compiled, 0 failed |
| Diff | `git diff --check` | PASS | line-ending warnings only |
| Secret scan | targeted `rg` | PASS after inspection | policy/test/template matches only |

## Coverage Quality

Strongest coverage:

- command smoke and report shape checks
- verifier structural checks
- golden-task local packet quality checks
- no-call/no-secret provider and Gateway checks

Weakest coverage:

- real coding task quality
- cross-repo behavior
- exact token accounting
- semantic route quality
- review-outcome tracking

## Test Runner Finding

The direct tests are healthy. The official-looking discovery command fails
because `.aide` is not importable as a package. This should be fixed before
asking future agents to rely on one command.
