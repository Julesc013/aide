# PatchTransaction Acceptance Status

Result: `BLOCKED`

PatchTransaction is not accepted.

The live independent check did not pass:

```text
AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01
result: FAILED_VALIDATION
recommended_next_task: AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01
```

The failed check is preserved. The only serialized next task is:

```text
AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01
```
