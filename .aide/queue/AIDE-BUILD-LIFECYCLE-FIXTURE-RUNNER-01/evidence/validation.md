# Validation

| Command | Result | Notes |
| --- | --- | --- |
| `py -3 -m unittest discover -s .aide\scripts\tests -p test_aide_lifecycle_fixture_runner.py` | PASS | 7 tests passed, including parser registration, temp-only mutation, fail-closed verification, CLI smoke, and path-jail rejection. |
| `py -3 -m unittest core.apply.tests.test_transaction_executor core.apply.tests.test_managed_sections` | PASS | 37 existing apply tests passed. |
| `py -3 .aide\scripts\aide_lite.py lifecycle-fixture status` | PASS | Wrote lifecycle fixture runner status report. |
| `py -3 .aide\scripts\aide_lite.py lifecycle-fixture run --scenario install-managed-section --mode apply-temp` | PASS | Mutated `.aide/reports/lifecycle-fixture-runner/workspaces/latest/**` only; reported `canonical_fixture_mutated: false`. |
| `py -3 .aide\scripts\aide_lite.py lifecycle-fixture verify` | PASS | 15 verification checks passed for latest completed run. |
| `py -3 .aide\scripts\aide_lite.py task inspect --task-id AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-01` | PASS | Task is `needs_review`, classified complete, with no missing evidence. |
| `py -3 .aide\scripts\aide_lite.py task evidence --task-id AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-01` | PASS | Six evidence files are available; none missing. |
| `git diff -- .aide\examples\apply\lifecycle-fixtures\target\existing-managed-section .aide\examples\apply\lifecycle-fixtures\expected\install-managed-section .aide\examples\apply\lifecycle-fixtures\generated-plans\install-managed-section.plan.json .aide\examples\apply\lifecycle-fixtures\expected-reports\install-managed-section.report.json .aide\examples\apply\lifecycle-fixtures\rollback-records\install-managed-section.rollback.json` | PASS | No diff; canonical fixture inputs and static records unchanged. |
| `py -3 .aide\scripts\aide_lite.py intent validate` | PASS | Intake artifacts validate. |
| `git diff --check` | PASS | No whitespace errors before and after root planning/execution/documentation log updates. |
| `py -3 .aide\scripts\aide_lite.py validate` | FAIL then PASS | Initial failure was `latest task packet missing section: TOKEN_ESTIMATE`; after adding `TOKEN_ESTIMATE`, validation passed. |
| `py -3 .aide\scripts\aide_lite.py test` | PASS | Full AIDE Lite test command passed after root log updates. |

Validation gaps:

- Commit validation is deferred until an actual commit is created.
- Independent review is deferred to `AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-CHECK-01`.
