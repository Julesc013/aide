# CLI Review

Status: `PASS`

Accepted Reconciler CLI surface:

- `py -3 .aide/scripts/aide_lite.py reconciler status`
- `py -3 .aide/scripts/aide_lite.py reconciler report`
- `py -3 .aide/scripts/aide_lite.py reconciler validate`

CLI boundary:

- Dispatch remains thin in `.aide/scripts/aide_lite.py`.
- Implementation lives in `core/reconciler/reconciler_reports.py`.
- Unsupported Reconciler subcommands fail closed or are absent.

Not implemented:

- `reconciler repair`
- `reconciler apply`
- `reconciler fix`
- `reconciler clean`
- `reconciler accept`
- `reconciler supersede`
- `reconciler schedule`
- `reconciler run-loop`
- `reconciler daemon`

The CLI does not implement runtime, CapabilityManifest, PatchTransaction, adapters, ContextPack, Service, Commander, provider, network, Gateway, GitHub, branch/worktree, target apply, active apply, release, or promotion behavior.
