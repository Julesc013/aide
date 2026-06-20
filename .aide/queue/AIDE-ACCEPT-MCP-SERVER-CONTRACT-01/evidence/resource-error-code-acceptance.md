# Resource Error-Code Acceptance

Accepted repaired behavior:

- `resource-not-found-refusal.json` uses JSON-RPC error code `-32002`.
- The message remains resource-not-found specific.
- The fixture remains a JSON-RPC error response.
- The fixture index and repair-check report agree on `-32002`.
- Regression probes confirmed restoring `-32043` fails validation.
