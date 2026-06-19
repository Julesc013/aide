# AIDE-ACCEPT-PATCH-TRANSACTION-SCHEMA-01

Acceptance/consolidation gate for the minimal PatchTransaction protocol slice.

Live queue truth controls execution. If the build and independent check are
complete and the check passed, this task may accept only the schema-only
representation/projection/validation capability.

If the independent check reports `FAILED_VALIDATION`, `BLOCKED`, or recommends
a repair, this task must stop as `BLOCKED`, preserve the failed check, identify
the authorized repair task, and recommend only that repair task.

Live disposition for this run:

```text
AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01
result: FAILED_VALIDATION
recommended_next_task: AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01
```

PatchTransaction is not accepted by this task.
