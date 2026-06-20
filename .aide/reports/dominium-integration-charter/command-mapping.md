# Command Mapping

Future AIDE invocation envelope:

```text
AIDE intent/work
-> registered Dominium command ID
-> capability/refusal check
-> service or deterministic process
-> typed result/refusal
-> diagnostic/evidence
-> view/action projection
```

Required refs:

- command correlation ID
- WorkUnit ref
- ContextPack ref
- future principal ref
- future grant ref
- future invocation ref
- result/refusal ref
- evidence refs
- event refs

No command invocation is implemented by this task. The first validation slice may only form a deterministic intent against an existing Dominium validation command when a later queue task explicitly authorizes it.
