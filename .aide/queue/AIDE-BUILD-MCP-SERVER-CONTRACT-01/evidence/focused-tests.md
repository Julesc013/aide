# Focused Tests

Command:

```text
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_mcp_server_contract.py
```

Result:

```text
Ran 41 tests
OK
```

Coverage includes protocol and JSON-RPC version pinning, lifecycle fixtures,
resource URI validation, duplicate resource rejection, tool-name validation,
read-only tool boundaries, tool-call refusal, prompt catalogue structure,
transport and authorization non-implementation, runtime facts, deterministic
projection, source immutability, unsupported execution subcommands, static MCP
preview consistency, and explicit non-capabilities.
