# Validation

Result: `ACCEPTED_WITH_WARNINGS`

Preflight:

| Command | Exit | Result | Notes |
| --- | ---: | --- | --- |
| `git status --short --branch` | 0 | PASS | initial status clean on `main...origin/main` |
| `git remote -v` | 0 | PASS | origin configured |
| `git rev-parse HEAD` | 0 | PASS | `2a1baf8c6145337f4e6155f5872aa6b517b10675` |
| `git show --stat --oneline --name-status HEAD` | 0 | PASS | check commit |
| `git show --stat --oneline --name-status 0c10e02a2dc4536d508670c1821770bf37d53b3e` | 0 | PASS | build commit exists |
| `git show --stat --oneline --name-status 2a1baf8c6145337f4e6155f5872aa6b517b10675` | 0 | PASS | check commit exists |
| `git show --stat --oneline --name-status 337acb983cb76286f98f9a60118f91ef263668cf` | 0 | PASS | predecessor acceptance commit exists |
| `git diff --check HEAD^ HEAD` | 0 | PASS | no whitespace errors |

Dynamic validation:

| Command | Exit | Result | Notes |
| --- | ---: | --- | --- |
| `py -3 .aide/scripts/aide_lite.py task status` | 0 | PASS | generated status churn restored |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-EVIDENCE-PACKET-SCHEMA-01` | 0 | PASS | build task inspect |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-EVIDENCE-PACKET-SCHEMA-01` | 0 | PASS | check task inspect |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-EVIDENCE-PACKET-SCHEMA-01` | 0 | PASS | check evidence inspect |
| `py -3 .aide/scripts/aide_lite.py evidence-packet status` | 0 | PASS | status report |
| `py -3 .aide/scripts/aide_lite.py evidence-packet project --source accepted-slices` | 0 | PASS | five projections |
| `py -3 .aide/scripts/aide_lite.py evidence-packet validate` | 0 | PASS | schema/helper/projection validation |
| `py -3 .aide/scripts/aide_lite.py contract-envelope status` | 0 | PASS | compatibility |
| `py -3 .aide/scripts/aide_lite.py contract-envelope project --source lifecycle-fixture-runner` | 0 | PASS | compatibility |
| `py -3 .aide/scripts/aide_lite.py contract-envelope validate` | 0 | PASS | compatibility |
| `py -3 .aide/scripts/aide_lite.py lifecycle-fixture status` | 0 | PASS | compatibility |
| `py -3 .aide/scripts/aide_lite.py lifecycle-fixture run --scenario install-managed-section --mode apply-temp` | 0 | PASS | temp workspace only |
| `py -3 .aide/scripts/aide_lite.py lifecycle-fixture verify` | 0 | PASS | compatibility |
| `py -3 .aide/scripts/aide_lite.py validate` | 0 | PASS | broad validation |
| `py -3 .aide/scripts/aide_lite.py test` | 0 | PASS | broad tests |

Unavailable:

- `py -3 -c "import yaml"`: exit 1, `ModuleNotFoundError: No module named 'yaml'`.

Non-blocking because repo-native validation, task inspection, JSON parsing, and
stdlib structural checks passed.
