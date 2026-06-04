# Validation

This file records the validation commands run for `AIDE-LIFECYCLE-SCHEMA-VALIDATOR-01`.

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short --branch` | PASS | Preflight clean before required status commands refreshed reports. |
| `git remote -v` | PASS | Origin fetch/push remote reported. |
| `git rev-parse HEAD` | PASS | Initial HEAD `7d6bf4fd0ae57918ee8e83bca1d9edf039916013`. |
| `git show --stat --oneline --name-status HEAD` | PASS | HEAD is lifecycle schema/fixture planning commit. |
| `git diff --check HEAD^ HEAD` | PASS | No whitespace errors in prior commit. |
| `py -3 .aide/scripts/aide_lite.py task status` | PASS | Wrote task status report. |
| `py -3 .aide/scripts/aide_lite.py task next-plan` | PASS_WITH_WARNING | Still selects `AIDE-APPLY-LIFECYCLE-PLAN-01`; task-local upstream next batch selects this validator. |
| `py -3 .aide/scripts/aide_lite.py task inspect AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01` | NOT_RUN | Positional form is unsupported and returned an argument error. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01` | PASS | Upstream task classified complete. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01` | PASS | Upstream evidence files listed. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | Repo validation passed after validator hook existed; lifecycle schema checks and reports passed. |
| `py -3 .aide/scripts/aide_lite.py scoped-transaction status` | PASS | Report-only status; no target mutation. |
| `py -3 .aide/scripts/aide_lite.py managed-section status` | PASS | Report-only status; no active repo apply. |
| `py -3 .aide/scripts/aide_lite.py transaction status` | PASS | Report-only status; no real repo apply. |
| `py -3 -c "import json; print('json: available')"` | PASS | Stdlib JSON available. |
| `py -3 -c "import jsonschema; print('jsonschema: available')"` | NOT_RUN | Module probe failed with `ModuleNotFoundError`; fallback validator used. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema status` | PASS | Wrote lifecycle schema status reports. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema validate` | PASS | 280 checks passed after import-detection fix. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema fixture-verify` | PASS | 298 checks passed. |
| `py -3 -m unittest .aide/scripts/tests/test_aide_lifecycle_schema_validator.py` | NOT_RUN | Python unittest path-style invocation failed with `ValueError: Empty module name`. |
| `py -3 .aide/scripts/tests/test_aide_lifecycle_schema_validator.py` | PASS | 10 tests passed. |
| `py -3 -m py_compile .aide/scripts/aide_lite.py` | PASS | Script compiles. |
| `git diff --check` | PASS | No whitespace errors in working-tree diff. |
| `git diff --cached --check` | PASS | No staged diff existed; command passed. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-SCHEMA-VALIDATOR-01` | PASS | New task classified complete with no missing evidence. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-SCHEMA-VALIDATOR-01` | PASS | New task evidence files listed. |
| JSON parse check over lifecycle schemas, examples, and lifecycle-schema reports | PASS | 12 JSON files parsed. |
| `py -3 -c "import yaml; print('pyyaml: available')"` | NOT_RUN | PyYAML unavailable; structural YAML key check used. |
| structural YAML key check | PASS | Queue task/status/index files contain required structural keys. |
| positive boundary text search | PASS | Required schema, fixture, report mode, dry-run, path, rollback, preimage/postimage, and review-gate markers found. |
| prohibited boundary text search | PASS | Prohibited terms appear in blocked/prohibited/not-performed contexts. |
| changed-surface secret scan | PASS_WITH_NOTES | Hits are secret-scanner implementation/test marker strings in `.aide/scripts/aide_lite.py`, not live credentials. |
