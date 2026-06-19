# Check Report

Result: `BLOCKED`

The ContextPack v2 independent check was not executed. Live queue truth does
not satisfy the prompt's execution-order gate:

- `AIDE-BUILD-CONTEXTPACK-V2-01`: `BLOCKED`
- `AIDE-ACCEPT-ADAPTER-MANIFEST-01`: `BLOCKED`
- `AIDE-ACCEPT-PATCH-TRANSACTION-SCHEMA-01`: `BLOCKED`

No ContextPack v2 implementation was checked. The exact serialized next task is:

```text
AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01
```
