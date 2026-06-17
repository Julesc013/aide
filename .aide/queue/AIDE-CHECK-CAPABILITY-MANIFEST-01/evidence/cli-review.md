# CLI Review

Finding: pass.

Registered commands:

```powershell
py -3 .aide/scripts/aide_lite.py capability-manifest status
py -3 .aide/scripts/aide_lite.py capability-manifest project
py -3 .aide/scripts/aide_lite.py capability-manifest validate
```

Dispatch remains thin:

- `aide_lite.py` loads `core/protocol/capability_manifest.py`.
- `status`, `project`, and `validate` delegate to the helper.

Unsupported verbs fail closed with exit code 2:

- `run`
- `execute`
- `admit`
- `conformance`
- `adapter-run`
- `repair`
- `mutate`

No CLI command implements ConformanceProfile, adapter admission,
PatchTransaction, runtime, Service, or Commander behavior.
