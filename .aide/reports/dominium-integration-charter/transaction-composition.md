# Transaction Composition

Layered model:

```text
PatchTransaction
  current AIDE file-oriented no-apply proposal

DevelopmentTransaction
  future generic AIDE governance envelope

DomainMutationBundle
  Dominium-owned domain operation payload

PreviewSession / ShadowWorkspace
  future disposable validation boundary

Owning Dominium/Domino process
  authoritative apply/undo

Workbench
  preview, approval, and host-authoritative apply request
```

This task does not extend PatchTransaction. Domain payloads remain Dominium-owned. Apply and undo remain owned by Dominium/Domino process surfaces, not AIDE or Workbench projection.
