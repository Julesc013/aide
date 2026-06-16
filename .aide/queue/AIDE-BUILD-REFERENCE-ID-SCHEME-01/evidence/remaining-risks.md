# Remaining Risks

- Full JSON Schema Draft 2020-12 validation is not implemented; the helper uses the local minimal subset pattern already used by nearby protocol slices.
- ReferenceID does not resolve objects at runtime; it only validates and projects stable identifiers and optional locators.
- Future object protocols such as EventRecord, OKF, PatchTransaction, AdapterManifest, and ContextPack v2 remain undefined by this task.
- The filesystem queue still needs independent check review before acceptance.
- `.aide/context/latest-task-packet.md` remains stale relative to live queue truth.
