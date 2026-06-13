# Validation

Validation passed with warnings limited to intentional deferrals and accepted predecessor warning posture.

| Command | Exit | Result |
| --- | ---: | --- |
| `git diff --check` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py workunit status` | 0 | PASS, 116 discovered and projectable queue tasks |
| `py -3 .aide/scripts/aide_lite.py workunit list` | 0 | PASS, read-only list report written |
| `py -3 .aide/scripts/aide_lite.py workunit inspect --task-id AIDE-BUILD-WORKUNIT-QUEUE-V1-01` | 0 | PASS, projected WorkUnit valid |
| `py -3 .aide/scripts/aide_lite.py workunit validate` | 0 | PASS, 116 WorkUnit objects validated |
| `py -3 .aide/scripts/aide_lite.py workunit-queue status` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py workunit-queue project --source queue-tasks` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py workunit-queue validate` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py evidence-packet status` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py evidence-packet project --source accepted-slices` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py evidence-packet validate` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py contract-envelope status` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py contract-envelope project --source lifecycle-fixture-runner` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py contract-envelope validate` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py lifecycle-fixture status` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py lifecycle-fixture run --scenario install-managed-section --mode apply-temp` | 0 | PASS, temp-only fixture mutation |
| `py -3 .aide/scripts/aide_lite.py lifecycle-fixture verify` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py validate` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py test` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-WORKUNIT-CLI-01` | 0 | PASS, complete, 11 evidence files |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-WORKUNIT-CLI-01` | 0 | PASS, missing 0 |

Report parsing:

- `.aide/reports/workunit-cli/list.json`: PASS
- `.aide/reports/workunit-cli/inspect/AIDE-BUILD-WORKUNIT-QUEUE-V1-01.json`: PASS
- `.aide/reports/workunit-cli/validation.json`: PASS
- `.aide/reports/workunit-queue/validation.json`: PASS
- `.aide/reports/evidence-packet/validation.json`: PASS
- `.aide/reports/contract-envelope/validation.json`: PASS
- `.aide/reports/lifecycle-fixture-runner/verify.json`: PASS

Structural YAML parsing:

- `.aide/queue/AIDE-BUILD-WORKUNIT-CLI-01/task.yaml`: PASS
- `.aide/queue/AIDE-BUILD-WORKUNIT-CLI-01/status.yaml`: PASS
- `.aide/queue/index.yaml`: PASS

WorkUnit CLI validation facts:

- `capability_label`: `minimal_workunit_readonly_cli`
- `workunit_cli_mode`: `readonly`
- `source_queue_tasks_checked`: 116
- `workunit_objects_validated`: 116
- `source_queue_tasks_mutated`: false
- `destructive_migration_performed`: false
- path traversal, absolute path, separator injection, wildcard, and hidden path checks rejected unsafe ids
- unknown optional fields tolerated
- unknown required capability fails closed
- explicit non-capabilities preserved
