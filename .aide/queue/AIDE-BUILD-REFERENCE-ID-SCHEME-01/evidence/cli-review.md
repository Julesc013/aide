# CLI Review

CLI commands added:

- `py -3 .aide/scripts/aide_lite.py reference-id status`
- `py -3 .aide/scripts/aide_lite.py reference-id project`
- `py -3 .aide/scripts/aide_lite.py reference-id validate`

Observed behavior:

- Commands load `core/protocol/reference_id.py` through the same thin module-loader pattern used by WorkerRun and TestJob.
- `project` defaults to `--source accepted-protocol`.
- Commands print explicit boundary lines showing runtime registry, resolver service, EventRecord, OKF, PatchTransaction, adapter manifest, target mutation, active apply, branch mutation, provider/model calls, Gateway calls, network calls, and GitHub mutation are not implemented/performed.

Boundary:

- CLI commands write only `.aide/reports/reference-id/**` reports and do not perform runtime resolution, repository apply behavior, network calls, provider calls, or branch mutation.
