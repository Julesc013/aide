# AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-01 ExecPlan

## Objective

Independently check `AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01` without
repairing implementation, accepting `distribution_manifest_v1`, or beginning
`ProjectLock v0`.

## Scope

- Re-read live queue truth and the Repair 01 source task.
- Inspect the repair task's self-hosted turn files and nine-finding matrix.
- Run a task-local independent checker for the nine repaired findings:
  extension boundary, identity/status boundary, component graph, artifact
  integrity, pre-access path safety, checksum value verification, protocol range
  semantics, source contamination, and fixture coverage.
- Run focused and broad validation commands and record receipts.
- Stop at `needs_review`.

## Allowed Paths

- `.aide/queue/AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-01/**`
- `.aide/reports/distribution-manifest-v1-repair-01-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

## Forbidden Paths

- `.aide/protocol/aide-distribution-manifest-v1.schema.json`
- `core/protocol/distribution_manifest.py`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_distribution_manifest_v1.py`
- `.aide/fixtures/distribution-manifest-v1/**`
- `.aide/reports/distribution-manifest-v1/**`
- Q43-Q48 implementation outputs except read-only validation commands
- target repositories

## Verification Intent

Run the task-local checker and the validation matrix. If any material finding
remains, route exactly to `AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-02` and
stop the wave. If no material finding remains, route exactly to
`AIDE-ACCEPT-DISTRIBUTION-MANIFEST-V1-01`.

## Review Gate

Stop at `needs_review`.
