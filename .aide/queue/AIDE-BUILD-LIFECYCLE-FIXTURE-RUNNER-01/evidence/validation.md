# Validation

| Command | Result | Notes |
| --- | --- | --- |
| `git remote -v` | PASS | `origin` fetch/push remote is `https://github.com/Julesc013/aide.git`. |
| `git rev-parse HEAD` | PASS | Pre-gap-fix HEAD was `47c0eb9dbb15012ce2d9cabdab2350946e0005eb`. |
| `git show --stat --oneline --name-status HEAD` | PASS | Latest committed build slice is `47c0eb9 feat(harness): add lifecycle fixture temp runner`. |
| `git diff --check HEAD^ HEAD` | PASS | Previous build-slice commit has no whitespace errors. |
| `py -3 -m py_compile .aide\scripts\aide_lite.py core\apply\lifecycle_fixture_runner.py` | PASS | CLI and runner module compile. |
| `py -3 -m unittest discover -s .aide\scripts\tests -p test_aide_lifecycle_fixture_runner.py` | PASS | 12 tests passed, including parser registration, temp-only mutation, fail-closed verification, report aliases, unsupported scenario/mode rejection, rollback non-execution, CLI dispatch boundary, and path-jail rejection. |
| `py -3 -m unittest core.apply.tests.test_transaction_executor core.apply.tests.test_managed_sections` | PASS | 37 existing apply tests passed. |
| `py -3 .aide\scripts\aide_lite.py lifecycle-fixture status` | PASS | Wrote lifecycle fixture runner status report. |
| `py -3 .aide\scripts\aide_lite.py lifecycle-fixture run --scenario install-managed-section --mode apply-temp` | PASS | Mutated `.aide/reports/lifecycle-fixture-runner/workspaces/latest/**` only; reported `canonical_fixture_mutated: false`. |
| `py -3 .aide\scripts\aide_lite.py lifecycle-fixture verify` | PASS | 17 verification checks passed for latest completed run. |
| `py -3 .aide\scripts\aide_lite.py task status` | PASS | Latest task is `AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-01`; command is report-only. |
| `py -3 .aide\scripts\aide_lite.py lifecycle-schema status` | PASS | Report-only lifecycle schema status passed. |
| `py -3 .aide\scripts\aide_lite.py lifecycle-schema validate` | PASS | 280 lifecycle schema checks passed with stdlib structural fallback. |
| `py -3 .aide\scripts\aide_lite.py lifecycle-schema fixture-verify` | PASS | 298 fixture shape checks passed. |
| `py -3 .aide\scripts\aide_lite.py scoped-transaction status` | PASS | Scoped transaction status passed; target repo capable false, broad active repo apply false. |
| `py -3 .aide\scripts\aide_lite.py managed-section status` | PASS | Managed-section status passed; active repo apply false. |
| `py -3 .aide\scripts\aide_lite.py transaction status` | PASS | Transaction status passed; real repo apply false and fixture-only planning true. |
| `py -3 .aide\scripts\aide_lite.py task inspect --task-id AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-01` | PASS | Task is `needs_review`, classified complete, with no missing evidence. |
| `py -3 .aide\scripts\aide_lite.py task evidence --task-id AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-01` | PASS | Twelve evidence files are available; none missing. |
| `git diff -- .aide\examples\apply\lifecycle-fixtures\target\existing-managed-section .aide\examples\apply\lifecycle-fixtures\expected\install-managed-section .aide\examples\apply\lifecycle-fixtures\generated-plans\install-managed-section.plan.json .aide\examples\apply\lifecycle-fixtures\expected-reports\install-managed-section.report.json .aide\examples\apply\lifecycle-fixtures\rollback-records\install-managed-section.rollback.json` | PASS | No diff; canonical fixture inputs and static records unchanged. |
| `py -3 .aide\scripts\aide_lite.py intent validate` | PASS | Intake artifacts validate. |
| JSON parse check for lifecycle fixture reports | PASS | Parsed seven generated JSON files: status, latest-run, run-report, latest-verify, verify, latest transaction plan, and rollback-compatible record. |
| YAML-like structural check for changed task/status/index files | PASS | Checked three YAML-like files for tab-free structure. |
| overclaiming scan | PASS | No true `production_ready`, `release_ready`, `service_ready`, `commander_ready`, `provider_adapter_ready`, `target_repo_mutated`, `active_repo_apply_mutation`, or `rollback_executed` values in runner/task/report scope. |
| obvious secret marker scan | PASS | No raw prompt/body, private-key, provider-key, or `sk-ant` markers in runner/task/report scope. |
| `git diff --cached --check` | PASS | No staged whitespace errors at the time checked. |
| `git diff --check` | PASS | No whitespace errors before and after root planning/execution/documentation log updates. |
| `py -3 .aide\scripts\aide_lite.py validate` | FAIL then PASS | Initial failure was `latest task packet missing section: TOKEN_ESTIMATE`; after adding `TOKEN_ESTIMATE`, validation passed. |
| `py -3 .aide\scripts\aide_lite.py test` | PASS | Full AIDE Lite test command passed after root log updates and the attached-prompt alignment pass. |

Validation gaps:

- Independent review is deferred to `AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-CHECK-01`.
- Commit validation is run after each local queue-work commit.
