# AIDE-BUILD-WORKER-RUN-SCHEMA-01

Build the minimal WorkerRun schema slice as data only.

Introduce `minimal_worker_run_schema` for metadata-only WorkerRun records projected from accepted validation/check/acceptance artifacts. Keep the implementation narrow and additive. Do not execute workers, claim WorkUnits, create leases, schedule work, invoke providers, submit tests, mutate targets, apply patches, roll back, promote, release, or call network/Gateway/GitHub/model surfaces.

Required commands:

```text
py -3 .aide/scripts/aide_lite.py worker-run status
py -3 .aide/scripts/aide_lite.py worker-run project --source accepted-artifacts
py -3 .aide/scripts/aide_lite.py worker-run validate
```

End at `needs_review` with evidence and recommend `AIDE-CHECK-WORKER-RUN-SCHEMA-01`.
