# Refusal, Transport, And Authorization Review

Refusal fixtures are JSON-RPC error responses. Custom AIDE refusal codes are
acceptable for AIDE-specific refusal conditions.

The resource-not-found mapping is not acceptable as generated because the
pinned MCP mapping is `-32002`, not `-32043`.

Transport profiles for stdio and Streamable HTTP are static expectations only.
Authorization expectations are static future concerns only.

No server, subprocess, socket, HTTP request, SSE stream, session, OAuth flow,
token handling, or credential resolution occurred.
