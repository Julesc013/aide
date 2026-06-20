# Warning Disposition

Warnings are retained but non-blocking:

- no vendored full official MCP schema;
- no live MCP server, stdio transport, or Streamable HTTP transport;
- no authorization implementation;
- no resource or prompt serving;
- no tool execution;
- no MCP tasks, sampling, or elicitation;
- advisory future `aide://interop` ReferenceID warning debt;
- inherited report and generated-output warning debt;
- production validator diagnostics do not print every observed invalid type,
  though injected-case evidence records those types.

The repaired safety cases fail closed.
