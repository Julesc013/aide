# Validation

Result: `PASS_WITH_WARNINGS`

Preflight:

| Command | Exit | Result | Notes |
| --- | ---: | --- | --- |
| `git status --short --branch` | 0 | PASS | initial status clean on `main...origin/main` |
| `git remote -v` | 0 | PASS | origin configured |
| `git rev-parse HEAD` | 0 | PASS | `0c10e02a2dc4536d508670c1821770bf37d53b3e` |
| `git show --stat --oneline --name-status HEAD` | 0 | PASS | EvidencePacket build commit |
| `git show --stat --oneline --name-status 0c10e02a2dc4536d508670c1821770bf37d53b3e` | 0 | PASS | reported implementation commit exists |
| `git show --stat --oneline --name-status 337acb983cb76286f98f9a60118f91ef263668cf` | 0 | PASS | predecessor acceptance commit exists |
| `git diff --check HEAD^ HEAD` | 0 | PASS | no whitespace errors |
| `py -3 .aide/scripts/aide_lite.py task status` | 0 | PASS | generated status churn inspected and restored |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-EVIDENCE-PACKET-SCHEMA-01` | 0 | PASS | complete, no missing evidence |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-EVIDENCE-PACKET-SCHEMA-01` | 0 | PASS | 12 evidence files |

Dynamic validation:

| Command | Exit | Result | Notes |
| --- | ---: | --- | --- |
| `py -3 .aide/scripts/aide_lite.py evidence-packet status` | 0 | PASS | status report |
| `py -3 .aide/scripts/aide_lite.py evidence-packet project --source accepted-slices` | 0 | PASS | 5 projections |
| `py -3 .aide/scripts/aide_lite.py evidence-packet validate` | 0 | PASS | schema/helper/projection validation |
| `py -3 .aide/scripts/aide_lite.py contract-envelope status` | 0 | PASS | compatibility |
| `py -3 .aide/scripts/aide_lite.py contract-envelope project --source lifecycle-fixture-runner` | 0 | PASS | compatibility |
| `py -3 .aide/scripts/aide_lite.py contract-envelope validate` | 0 | PASS | compatibility |
| `py -3 .aide/scripts/aide_lite.py lifecycle-fixture status` | 0 | PASS | compatibility |
| `py -3 .aide/scripts/aide_lite.py lifecycle-fixture run --scenario install-managed-section --mode apply-temp` | 0 | PASS | temp workspace only |
| `py -3 .aide/scripts/aide_lite.py lifecycle-fixture verify` | 0 | PASS | 48 checks |
| `py -3 .aide/scripts/aide_lite.py validate` | 0 | PASS | broad AIDE Lite validation |
| `py -3 .aide/scripts/aide_lite.py commit check --latest` | 0 | PASS | build commit message policy |

Negative validation:

| Command or check | Exit | Result | Notes |
| --- | ---: | --- | --- |
| `py -3 .aide/scripts/aide_lite.py evidence-packet project --source does-not-exist` | 2 | PASS | unsupported source rejected by parser |
| `py -3 .aide/scripts/aide_lite.py evidence-packet project` | 2 | PASS | missing required `--source` rejected |
| in-memory missing field checks | 0 | PASS | required fields reject |
| in-memory unknown optional field check | 0 | PASS | tolerated |
| in-memory unknown required capability check | 0 | PASS | fails closed |
| temp malformed schema alignment check | 0 | PASS | fails closed |

Unavailable:

- `py -3 -c "import yaml"`: exit 1, `ModuleNotFoundError: No module named 'yaml'`.

This is non-blocking because AIDE task inspection, AIDE validation, JSON parsing,
and stdlib structural checks passed.
