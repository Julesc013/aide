# Focused Tests

Command:

```bash
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_mcp_server_contract.py
```

Result:

- `65` tests passed.

The suite includes pagination omission, cursor type rejection, resource-not-found code, custom refusal preservation, deterministic projection, source immutability, and unsupported command rejection coverage.
