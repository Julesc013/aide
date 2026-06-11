# Validation

## Preflight

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short --branch` | PASS | Initial status: `## main...origin/main`. |
| `git remote -v` | PASS | `origin` fetch/push remote is `https://github.com/Julesc013/aide.git`. |
| `git rev-parse HEAD` | PASS | `04b6b6c98058e31a5beae1548bb0e2d7a5381f24`. |
| `git show --stat --oneline --name-status HEAD` | PASS | HEAD is `04b6b6c fix(harness): align lifecycle fixture runner evidence`. |
| `git show --stat --oneline --name-status 04b6b6c` | PASS | Reported commit exists and is current. |
| `git diff --check HEAD^ HEAD` | PASS | No whitespace errors in checked commit. |
| `py -3 .aide/scripts/aide_lite.py task status` | PASS | Latest task is `AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-01`; report-only command refreshed task-os reports. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-01` | PASS | Checked task is `needs_review`, complete, evidence missing count 0. One unrelated PowerShell profile warning was printed after the command result. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-01` | PASS | Twelve evidence files available; none missing. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-fixture status` | PASS | Runner status passed. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-fixture verify` | PASS | Runner verify passed with 17 checks. |

## Dynamic Validation

| Command | Result | Notes |
| --- | --- | --- |
| `py -3 -m py_compile .aide/scripts/aide_lite.py core/apply/lifecycle_fixture_runner.py` | PASS | Compile check passed. |
| `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_lifecycle_fixture_runner.py` | PASS | 12 tests passed. |
| `py -3 -m unittest core.apply.tests.test_transaction_executor core.apply.tests.test_managed_sections` | PASS | 37 tests passed. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-fixture status` | PASS | Runner status passed. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-fixture run --scenario install-managed-section --mode apply-temp` | PASS | Fresh run passed; mutation scope is temp workspace only. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-fixture verify` | PASS | Verify passed with 17 checks. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema status` | PASS | Report-only schema status passed. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema validate` | PASS | 280 checks passed. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema fixture-verify` | PASS | 298 checks passed. |
| `py -3 .aide/scripts/aide_lite.py scoped-transaction status` | PASS | Scoped transaction status passed; target repo capable false. |
| `py -3 .aide/scripts/aide_lite.py managed-section status` | PASS | Managed-section status passed; active repo apply false. |
| `py -3 .aide/scripts/aide_lite.py transaction status` | PASS | Transaction status passed; real repo apply false. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | AIDE Lite validate passed. |
| `py -3 .aide/scripts/aide_lite.py test` | PASS | AIDE Lite test passed. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-01` | PASS | Checked task complete; no missing evidence. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-01` | PASS | Twelve evidence files available; none missing. |

## Negative Checks

| Command | Result | Notes |
| --- | --- | --- |
| `py -3 .aide/scripts/aide_lite.py lifecycle-fixture run --scenario does-not-exist --mode apply-temp` | PASS | Expected blocked exit code 2; argparse rejected unsupported scenario. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-fixture run --scenario install-managed-section --mode apply-active` | PASS | Expected blocked exit code 2; argparse rejected unsupported mode. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-fixture run --scenario install-managed-section --mode rollback` | PASS | Expected blocked exit code 2; argparse rejected unsupported rollback mode. |

## Machine Checks

| Check | Result | Notes |
| --- | --- | --- |
| JSON parse | PASS | Parsed latest-run, verify, rollback, status, and latest transaction-plan JSON. |
| Required report fields | PASS | Required latest-run and verify fields are present. |
| Report path scope | PASS | Mutable report paths stay under `.aide/reports/lifecycle-fixture-runner/**`; canonical refs point to read-only lifecycle fixtures. |
| Boundary hashes | PASS | Canonical target, expected postimage, and generated plan hashes were unchanged before/after fresh runner invocation; temp target hash matched expected postimage. |
| Overclaiming scan | PASS | Strict JSON boolean check found no forbidden true readiness/apply/rollback flags. |
| Secret scan | PASS | Strict token/private-key marker scan found no matches. |
| Canonical fixture diff | PASS | No diff for canonical target, expected state, generated plan, expected report, or static rollback record. |
| Branch/worktree state | PASS | Current branch is `main`; `git worktree list` shows only the current worktree. |
| `git diff --check` | PASS | No whitespace errors at check-writing time. |
