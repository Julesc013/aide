# Blocked Report

Result: `BLOCKED`

ContextPack v2 build was not executed. Live queue truth does not satisfy the
prompt's execution-order gate:

- `AIDE-ACCEPT-PATCH-TRANSACTION-SCHEMA-01`: `BLOCKED`
- `AIDE-BUILD-ADAPTER-MANIFEST-01`: `BLOCKED`
- `AIDE-CHECK-ADAPTER-MANIFEST-01`: `BLOCKED`
- `AIDE-ACCEPT-ADAPTER-MANIFEST-01`: `BLOCKED`

No ContextPack v2 capability is built. The exact serialized next task is:

```text
AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01
```
