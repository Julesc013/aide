# AIDE-BUILD-CONTEXTPACK-V2-01 Prompt

Build prompt for the deterministic, evidence-aware ContextPack v2 protocol
slice.

The prompt requires this task to stop as `BLOCKED` if AdapterManifest
acceptance is not `ACCEPTED` or `ACCEPTED_WITH_WARNINGS`, if AdapterManifest
task evidence is incomplete, if PatchTransaction acceptance is not accepted, or
if a later serialized next-task order blocks ContextPack v2 work.

Live queue truth controls this task. The live source chain is blocked, so this
task records a blocked build packet and recommends only:

```text
AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01
```
