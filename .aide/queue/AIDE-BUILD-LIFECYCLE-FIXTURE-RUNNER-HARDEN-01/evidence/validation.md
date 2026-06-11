# Validation

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short --branch` | PASS | HARDEN-01 started from clean worktree after CHECK-01 commit; branch was `main...origin/main [ahead 1]`. |
| `git rev-parse HEAD` | PASS | Starting HEAD was `3838724778283b70bd602e703e356084b16608cc`. |
| `py -3 .aide\scripts\aide_lite.py task inspect --task-id AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-CHECK-01` | PASS | CHECK-01 was complete and selected HARDEN-01. |
| `py -3 -m py_compile .aide\scripts\aide_lite.py core\apply\lifecycle_fixture_runner.py` | PASS | Compile check passed. |
| `py -3 -m unittest discover -s .aide\scripts\tests -p test_aide_lifecycle_fixture_runner.py` | PASS | 17 focused tests passed. |
| `py -3 -m unittest core.apply.tests.test_transaction_executor core.apply.tests.test_managed_sections` | PASS | 37 tests passed. |
| `py -3 .aide\scripts\aide_lite.py lifecycle-fixture status` | PASS | Runner status passed. |
| `py -3 .aide\scripts\aide_lite.py lifecycle-fixture run --scenario install-managed-section --mode apply-temp` | PASS | Fresh run passed; temp workspace only. |
| `py -3 .aide\scripts\aide_lite.py lifecycle-fixture verify` | PASS | Verify passed with 48 checks after hardening. |
| `py -3 .aide\scripts\aide_lite.py validate` | PASS | AIDE Lite validate passed. |
| `py -3 .aide\scripts\aide_lite.py test` | PASS | AIDE Lite test passed. |
| JSON parse check | PASS | Parsed latest-run, verify, and rollback record JSON. |
| Canonical fixture diff check | PASS | No diff for canonical target, expected state, generated plan, expected report, or static rollback record. |
| Overclaiming check | PASS | No forbidden readiness/apply/rollback true values in runner reports. |
| Secret marker scan | PASS | No token/private-key marker matches. |
| `git diff --check` | PASS | No whitespace errors. |
