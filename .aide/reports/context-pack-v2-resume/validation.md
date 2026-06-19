# ContextPack v2 Validation

- validation_status: PASS_WITH_WARNINGS

## Warnings
- ContextPack v2 is a deterministic projection only; it does not execute agents or commands.
- No model/provider/Gateway/network calls, embeddings, admission, trust, patch apply, target mutation, runtime, Service, Commander, or Workbench behavior exists.
- Pack sources are referenced by path and hash; no live resolver or event store exists.
