# Validation

Result: `PASS`

Commands:

- `py -3 .aide/scripts/aide_lite.py workunit-queue status` -> PASS
- `py -3 .aide/scripts/aide_lite.py workunit-queue project --source queue-tasks` -> PASS
- `py -3 .aide/scripts/aide_lite.py workunit-queue validate` -> PASS
- `py -3 .aide/scripts/aide_lite.py evidence-packet status` -> PASS
- `py -3 .aide/scripts/aide_lite.py evidence-packet project --source accepted-slices` -> PASS
- `py -3 .aide/scripts/aide_lite.py evidence-packet validate` -> PASS
- `py -3 .aide/scripts/aide_lite.py contract-envelope status` -> PASS
- `py -3 .aide/scripts/aide_lite.py contract-envelope project --source lifecycle-fixture-runner` -> PASS
- `py -3 .aide/scripts/aide_lite.py contract-envelope validate` -> PASS
- `py -3 .aide/scripts/aide_lite.py lifecycle-fixture status` -> PASS
- `py -3 .aide/scripts/aide_lite.py lifecycle-fixture run --scenario install-managed-section --mode apply-temp` -> PASS
- `py -3 .aide/scripts/aide_lite.py lifecycle-fixture verify` -> PASS
- `py -3 .aide/scripts/aide_lite.py validate` -> PASS
- `py -3 .aide/scripts/aide_lite.py test` -> PASS
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-WORKUNIT-QUEUE-V1-01` -> complete, missing evidence 0
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-WORKUNIT-QUEUE-V1-01` -> missing evidence 0
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-WORKUNIT-QUEUE-V1-01` -> complete, missing evidence 0
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-WORKUNIT-QUEUE-V1-01` -> missing evidence 0

`py -3 -c "import yaml"` failed because PyYAML is unavailable. This is
nonblocking because repo-native validation, JSON parsing, task inspection, and
stdlib structural checks passed.
