# Validation

| Command | Exit | Result | Notes |
| --- | ---: | --- | --- |
| `git status --short --branch` | 0 | PASS | Initial worktree clean on `main...origin/main`. |
| `git remote -v` | 0 | PASS | `origin` fetch/push remote present. |
| `git rev-parse HEAD` | 0 | PASS | Initial HEAD `a8af8a38053e6455b46c7afd81ac11cb682c3599`. |
| `git show --stat --oneline --name-status HEAD` | 0 | PASS | HEAD is HARDEN-01 commit `a8af8a3`. |
| `git show --stat --oneline --name-status 3838724` | 0 | PASS | CHECK-01 commit resolved. |
| `git show --stat --oneline --name-status a8af8a3` | 0 | PASS | HARDEN-01 commit resolved. |
| `git diff --check HEAD^ HEAD` | 0 | PASS | HARDEN-01 commit has no whitespace errors. |
| `py -3 .aide\scripts\aide_lite.py task status` | 0 | PASS | Required report-only command ran; generated task-os churn was restored because it was outside acceptance write scope. |
| `py -3 .aide\scripts\aide_lite.py task inspect --task-id AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-01` | 0 | PASS | Build task complete with no missing evidence. |
| `py -3 .aide\scripts\aide_lite.py task inspect --task-id AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-CHECK-01` | 0 | PASS | Check task complete with no missing evidence. |
| `py -3 .aide\scripts\aide_lite.py task inspect --task-id AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-HARDEN-01` | 0 | PASS | Harden task complete with no missing evidence. |
| `py -3 .aide\scripts\aide_lite.py task evidence --task-id AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-HARDEN-01` | 0 | PASS | Seven evidence files available; none missing. |
| `py -3 .aide\scripts\aide_lite.py lifecycle-fixture status` | 0 | PASS | Capability label `fixture_temp_apply_only`; no target, branch, provider, Gateway, or network behavior. |
| `py -3 .aide\scripts\aide_lite.py lifecycle-fixture run --scenario install-managed-section --mode apply-temp` | 0 | PASS | Temp workspace run passed; canonical fixture not mutated. |
| `py -3 .aide\scripts\aide_lite.py lifecycle-fixture verify` | 0 | PASS | 48 checks passed. |
| `py -3 .aide\scripts\aide_lite.py lifecycle-schema status` | 0 | PASS | Report-only status passed. |
| `py -3 .aide\scripts\aide_lite.py lifecycle-schema validate` | 0 | PASS | 280 structural checks passed. |
| `py -3 .aide\scripts\aide_lite.py lifecycle-schema fixture-verify` | 0 | PASS | 298 fixture checks passed. |
| `py -3 .aide\scripts\aide_lite.py scoped-transaction status` | 0 | PASS | Report-only status passed; no target mutation. |
| `py -3 .aide\scripts\aide_lite.py managed-section status` | 0 | PASS | Report-only status passed; active repo apply false. |
| `py -3 .aide\scripts\aide_lite.py transaction status` | 0 | PASS | Report-only status passed; real repo apply false. |
| `py -3 .aide\scripts\aide_lite.py validate` | 0 | PASS | AIDE Lite validate passed. |
| `py -3 .aide\scripts\aide_lite.py test` | 0 | PASS | AIDE Lite test passed. |

No required command was unavailable.
