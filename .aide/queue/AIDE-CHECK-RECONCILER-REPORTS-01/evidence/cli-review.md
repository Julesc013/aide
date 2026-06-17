# CLI Review

Status: `PASS`

Reviewed CLI behavior:

- `py -3 .aide/scripts/aide_lite.py reconciler status`
- `py -3 .aide/scripts/aide_lite.py reconciler report`
- `py -3 .aide/scripts/aide_lite.py reconciler validate`

Observed behavior:

- All three commands are report-only.
- The commands return `PASS_WITH_WARNINGS`.
- The commands report the expected non-capabilities and false mutation flags.
- No repair, apply, refresh, accept, runtime, provider, network, GitHub, branch, release, rollback, uninstall, or target mutation command was added for Reconciler.
