# stdio Expectation Review

The static stdio profile records:

- UTF-8 JSON-RPC messages
- newline-delimited messages
- no non-MCP output on stdout
- logging may use stderr
- client-launched subprocess model

Implementation status is `not_implemented`.

No subprocess was launched by the contract, no stdin/stdout protocol loop
exists, and no executable or command was installed.
