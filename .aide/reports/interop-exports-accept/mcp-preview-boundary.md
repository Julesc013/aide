# MCP Preview Boundary

`mcp-manifest.preview.json` is accepted only as structurally valid preview
metadata.

It records:

- `preview_only: true`
- `server_implemented: false`
- `transport: none`
- no tools
- disabled operations for mutation or external action

This acceptance is not:

- MCP server;
- MCP tool execution;
- MCP resource serving;
- MCP transport;
- MCP authentication;
- network access.
