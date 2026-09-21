# Validation

## Admission Checkpoint

| Command | Result |
|---|---|
| `py -3 -B .aide/scripts/aide_lite.py workunit validate` | PASS; 352 source queue tasks and WorkUnit objects validated |
| `py -3 -B .aide/scripts/aide_lite.py validate` | PASS |
| `git diff --check` | PASS |
| `git ls-remote --heads origin main dev task/aide-cw-integration-broker-01` | PASS; remote refs matched the recorded source and target heads |

The candidate-specific and post-integration checks remain pending. Refreshed
validator report snapshots were not retained because this task does not own
those generated paths.
