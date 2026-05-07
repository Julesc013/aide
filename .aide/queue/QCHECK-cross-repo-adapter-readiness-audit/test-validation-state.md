# Test And Validation State

## Canonical AIDE Lite Test Command

Canonical command:

```text
py -3 .aide/scripts/aide_lite.py test
```

Result: PASS.

The command is intentionally clearer than raw `unittest discover` and is the
recommended validation surface for copied AIDE Lite packs.

## Supported Raw Unittest Command

```text
py -3 -m unittest discover -s .aide/scripts/tests
```

Result: PASS, 112 tests.

## Invalid Legacy Command

```text
py -3 -m unittest discover -s .aide/scripts/tests -t .
```

Result: expected failure, exit 1.

Reason: Python's top-level package discovery rule treats the hidden `.aide`
path as a non-importable start directory when `-t .` is supplied. QFIX-02
documents this exact command as non-canonical rather than forcing a brittle
package layout.

## Core Tests

| Suite | Result | Count |
| --- | --- | ---: |
| `core/harness/tests` | PASS | 27 |
| `core/compat/tests` | PASS | 5 |
| `core/gateway/tests` | PASS | 9 |
| `core/providers/tests` | PASS | 8 |
| `.aide/scripts/tests` | PASS | 112 |

## AIDE Lite Command Sweep

The command sweep passed for doctor, validate, selftest/test, snapshot, index,
context, verify, review-pack, ledger, eval, routing, cache, Gateway, provider,
export-pack, and adapter commands. Advisory warnings were expected and recorded:

- `outcome report` warns that the current packet is too large.
- token ledger reports three near-budget surfaces.
- Harness self-check guidance still has minor followup drift.

## Reliability Assessment

AIDE Lite validation is now reliable enough for target repos if the imported
pack includes the same script/tests and users run the canonical `test` command.
The remaining risk is documentation drift: future prompts must stop telling
agents to use the invalid `-t .` command.
