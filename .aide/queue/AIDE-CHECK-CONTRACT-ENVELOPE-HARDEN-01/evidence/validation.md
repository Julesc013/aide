# Validation

| Command | Exit Code | Result | Notes |
| --- | ---: | --- | --- |
| `git status --short --branch` | 0 | PASS | Initial worktree was clean. |
| `git remote -v` | 0 | PASS | `origin` points to `https://github.com/Julesc013/aide.git`. |
| `git rev-parse HEAD` | 0 | PASS | `5d74bb500100e50a3dab31372d59e9afd24eec01`. |
| `git show --stat --oneline --name-status HEAD` | 0 | PASS | HEAD is reported hardening commit. |
| `git show --stat --oneline --name-status 5d74bb500100e50a3dab31372d59e9afd24eec01` | 0 | PASS | Reported hardening commit exists. |
| `git show --stat --oneline --name-status 1e5e0ff521beec77f141dd105bdcb2e569e6701a` | 0 | PASS | Predecessor check commit exists. |
| `git show --stat --oneline --name-status db3a1aba6289c955a68c55724e5e38c4622e62f1` | 0 | PASS | Predecessor build commit exists. |
| `git diff --check HEAD^ HEAD` | 0 | PASS | Hardening commit whitespace check passed. |
| `py -3 .aide/scripts/aide_lite.py task status` | 0 | PASS | Wrote task status report; generated churn restored after validation. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-CONTRACT-ENVELOPE-HARDEN-01` | 0 | PASS | Task complete, 11 evidence files, missing 0. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-CONTRACT-ENVELOPE-HARDEN-01` | 0 | PASS | All required HARDEN-01 evidence present. |
| `py -3 .aide/scripts/aide_lite.py contract-envelope status` | 0 | PASS | Status command passed. |
| `py -3 .aide/scripts/aide_lite.py contract-envelope project --source lifecycle-fixture-runner` | 0 | PASS | 3 projections written. |
| `py -3 .aide/scripts/aide_lite.py contract-envelope validate` | 0 | PASS | Schema loaded, parsed, subset validation executed, alignment PASS. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-fixture status` | 0 | PASS | Scope remains `fixture_temp_apply_only`. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-fixture run --scenario install-managed-section --mode apply-temp` | 0 | PASS | Temp-workspace run only. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-fixture verify` | 0 | PASS | 48 checks passed. |
| `py -3 .aide/scripts/aide_lite.py validate` | 0 | PASS | Repo validation passed. |
| `py -3 .aide/scripts/aide_lite.py test` | 0 | PASS | AIDE Lite test passed. |
| JSON parse checks | 0 | PASS | Schema, reports, projections, and lifecycle reports parsed. |
| PyYAML parse check | 2 | UNAVAILABLE | `yaml` module is not installed. |
| stdlib YAML structural check | 0 | PASS | Changed YAML files passed structural fallback checks. |
| overclaiming scan | 0 | PASS | No unsupported readiness/capability overclaims found. |
| lightweight secret marker scan | 0 | PASS | No obvious secret markers found. |

Result is capped at PASS_WITH_WARNINGS because PyYAML is unavailable, but the
gap is non-blocking: repo validation, task inspection, and stdlib structural
YAML checks passed.
