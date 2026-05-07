# Test And Validation State

## Harness

- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS, zero errors.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS, zero errors.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS, report-only, no
  mutation, no external calls.
- Harness tests: 27 tests pass.

Warnings are primarily old review gates and generated manifest/source
fingerprint drift. They do not indicate test failure.

## AIDE Lite

Canonical command:

```text
py -3 .aide/scripts/aide_lite.py test
```

Result: PASS.

Final structural validation warning:

- `py -3 .aide/scripts/aide_lite.py validate` fails after report writes because
  the committed export pack has a checksum mismatch for `manifest.yaml`.
- This does not invalidate the canonical test runner, which still passes.
- It does block broad pack handoff until Q25 or equivalent refreshes pack
  integrity from a clean HEAD.

Compatibility command:

```text
py -3 .aide/scripts/aide_lite.py selftest
```

Result: PASS.

Supported raw unittest command:

```text
py -3 -m unittest discover -s .aide/scripts/tests
```

Result: PASS, 112 tests.

Known invalid/non-canonical command:

```text
py -3 -m unittest discover -s .aide/scripts/tests -t .
```

Result: FAIL as expected with:

```text
ImportError: Start directory is not importable: 'D:\\Projects\\AIDE\\aide\\.aide\\scripts\\tests'
```

This is documented by QFIX-02. It fails because `.aide` is a hidden repo
contract directory, not an importable Python package namespace under repo-root
top-level discovery.

## Command Sweep

Passing AIDE Lite command families:

- doctor/validate
- snapshot/index/context
- verify/review-pack
- ledger scan/report
- eval list/run/report
- outcome report/optimize suggest
- route list/validate/explain
- cache status/report
- gateway status/endpoints/smoke
- provider list/status/validate/probe --offline
- export-pack during the dirty command sweep; final committed `pack-status`
  fails on `manifest.yaml` checksum
- adapter list/render/preview/validate/drift
- adapt

Nuance:

- `outcome report` returns WARN because advisory outcome ledger includes
  `packet_too_large`.
- `ledger scan` reports three near-budget warnings.
- Generated report commands temporarily dirtied latest artifacts during the
  audit. Those generated changes were restored and are recorded only as command
  evidence.

## Unit Tests

| Suite | Result |
| --- | --- |
| `core/harness/tests` | PASS, 27 tests |
| `core/compat/tests` | PASS, 5 tests |
| `core/gateway/tests` | PASS, 9 tests |
| `core/providers/tests` | PASS, 8 tests |
| `.aide/scripts/tests` | PASS, 112 tests |

PowerShell displayed `System.Management.Automation.RemoteException` around
some unittest stderr output while exit code stayed zero and unittest reported
`OK`; this is output wrapping, not a failing test.

## Reliability Verdict

The AIDE Lite test runner is reliable for AIDE itself. Full AIDE Lite
`validate` is currently blocked by export-pack checksum drift, and target
imports still need Q21 importer scope refinement because real target pilots
avoided direct apply after dry-run.
