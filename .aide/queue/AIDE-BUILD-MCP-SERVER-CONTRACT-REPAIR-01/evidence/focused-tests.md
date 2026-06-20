# Focused Tests

Focused MCP tests passed:

```text
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_mcp_server_contract.py
Ran 65 tests
OK
```

The test suite includes all prior MCP contract tests plus regressions for the
two failed-check findings.
