# Validation

| Command | Exit Code | Result | Notes |
| --- | ---: | --- | --- |
| `git status --short --branch` | 0 | PASS | Worktree contained only this task's expected edits and generated contract-envelope reports at validation time. |
| `git diff --check` | 0 | PASS | No whitespace errors. |
| `git diff --cached --check` | 0 | PASS | No staged whitespace errors; no files were staged. |
| `git diff --check HEAD^ HEAD` | 0 | PASS | Predecessor commit diff check passed. |
| `py -3 -m py_compile .aide/scripts/aide_lite.py core/protocol/envelope.py` | 0 | PASS | Compile check passed. |
| `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_contract_envelope.py` | 0 | PASS | 29 tests passed. |
| `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_lifecycle_fixture_runner.py` | 0 | PASS | 17 tests passed. |
| `py -3 -m unittest core.apply.tests.test_transaction_executor core.apply.tests.test_managed_sections` | 0 | PASS | 37 tests passed. |
| `py -3 .aide/scripts/aide_lite.py contract-envelope status` | 0 | PASS | Status command passed. |
| `py -3 .aide/scripts/aide_lite.py contract-envelope project --source lifecycle-fixture-runner` | 0 | PASS | Wrote 3 projections. |
| `py -3 .aide/scripts/aide_lite.py contract-envelope validate` | 0 | PASS | Reports schema loaded, parsed, subset validation executed, and helper/schema alignment PASS. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-fixture status` | 0 | PASS | Lifecycle fixture status remains scoped and non-mutating. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-fixture run --scenario install-managed-section --mode apply-temp` | 0 | PASS | Temp workspace run passed; generated lifecycle timestamp churn was restored after validation. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-fixture verify` | 0 | PASS | 48 checks passed; rollback remained unexecuted. |
| `py -3 .aide/scripts/aide_lite.py validate` | 0 | PASS | Repo validation passed. |
| `py -3 .aide/scripts/aide_lite.py test` | 0 | PASS | AIDE Lite internal test suite passed. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-CONTRACT-ENVELOPE-HARDEN-01` | 0 | PASS | Task is `needs_review`, classification `complete`, 11 evidence files, missing 0. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-CONTRACT-ENVELOPE-HARDEN-01` | 0 | PASS | All 11 evidence files present. |
| JSON parse check for schema, validation reports, projections, and lifecycle reports | 0 | PASS | All checked JSON files parsed. |
| PyYAML parse check for changed YAML files | 2 | UNAVAILABLE | `yaml` module is not installed in the environment. |
| stdlib structural YAML check for changed YAML files | 0 | PASS | Checked no tabs, non-empty roots, `schema_version`, and colon-bearing mapping/list lines. |
| canonical fixture diff check | 0 | PASS | No diff under `.aide/examples/apply/lifecycle-fixtures`. |
| overclaiming scan | 0 | PASS | No unsupported readiness/capability overclaims found. |
| lightweight secret marker scan | 0 | PASS | No obvious secret markers found. |

## Generated Churn Handling

The lifecycle fixture status/run/verify commands refreshed timestamp-only
reports under `.aide/reports/lifecycle-fixture-runner/`. Those files are not
deliverables for this task and were restored. `contract-envelope validate` was
then re-run so contract-envelope reports reflect committed lifecycle source
reports.
