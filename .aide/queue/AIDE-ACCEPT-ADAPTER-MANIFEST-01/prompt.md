# AIDE-ACCEPT-ADAPTER-MANIFEST-01 Prompt

Acceptance/consolidation prompt for the minimal provider-neutral
AdapterManifest protocol slice.

The prompt requires this task to stop as `BLOCKED` if the AdapterManifest build
or independent check is not complete with `PASS` or `PASS_WITH_WARNINGS`, if
their evidence is incomplete, if PatchTransaction acceptance is not accepted,
or if a repair task is the authorized next task.

Live queue truth controls this task. The live source chain is blocked, so this
task records a blocked acceptance packet and recommends only:

```text
AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01
```
