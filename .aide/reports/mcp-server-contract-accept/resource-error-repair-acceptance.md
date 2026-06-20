# Resource Error Repair Acceptance

The repaired resource-not-found mapping is accepted.

Facts:

- `resource-not-found-refusal.json` uses `error.code: -32002`;
- the fixture remains a JSON-RPC error response;
- the repair-check verified restoring `-32043` fails validation;
- fixture index and reports agree on `-32002`.

This closes the second material finding from the original failed check.
