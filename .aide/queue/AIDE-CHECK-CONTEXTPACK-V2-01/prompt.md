# AIDE-CHECK-CONTEXTPACK-V2-01 Prompt

Independent-check prompt for deterministic evidence-aware ContextPack v2.

The prompt requires this task to stop as `BLOCKED` if the build task is absent,
incomplete, contradicted, failed, superseded, or not `PASS` or
`PASS_WITH_WARNINGS`, or if AdapterManifest/PatchTransaction acceptance
preconditions are not accepted.

Live queue truth controls this task. The live source chain is blocked, so this
task records a blocked check packet and recommends only:

```text
AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01
```
