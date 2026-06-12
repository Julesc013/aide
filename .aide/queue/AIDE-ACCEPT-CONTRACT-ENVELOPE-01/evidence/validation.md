# Validation

| Command | Exit Code | Result | Notes |
| --- | ---: | --- | --- |
| `git status --short --branch` | 0 | PASS | Initial acceptance worktree clean; branch ahead one local check commit. |
| `git remote -v` | 0 | PASS | `origin` points to `https://github.com/Julesc013/aide.git`. |
| `git rev-parse HEAD` | 0 | PASS | `4060d56a3236353add27c7bd8de29e03016d2db3`. |
| `git show --stat --oneline --name-status db3a1aba6289c955a68c55724e5e38c4622e62f1` | 0 | PASS | Build commit exists. |
| `git show --stat --oneline --name-status 1e5e0ff521beec77f141dd105bdcb2e569e6701a` | 0 | PASS | Check commit exists. |
| `git show --stat --oneline --name-status 5d74bb500100e50a3dab31372d59e9afd24eec01` | 0 | PASS | Harden commit exists. |
| `git show --stat --oneline --name-status 4060d56a3236353add27c7bd8de29e03016d2db3` | 0 | PASS | Harden-check commit exists and was initial HEAD. |
| `git diff --check HEAD^ HEAD` | 0 | PASS | Harden-check commit whitespace check passed. |
| `py -3 .aide/scripts/aide_lite.py task status` | 0 | PASS | Generated status report refreshed; churn restored before commit. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-CONTRACT-ENVELOPE-01` | 0 | PASS | Complete, no missing evidence. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-CONTRACT-ENVELOPE-01` | 0 | PASS | Complete, no missing evidence. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-CONTRACT-ENVELOPE-HARDEN-01` | 0 | PASS | Complete, no missing evidence. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-CONTRACT-ENVELOPE-HARDEN-01` | 0 | PASS | Complete, no missing evidence. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-CONTRACT-ENVELOPE-HARDEN-01` | 0 | PASS | All 13 evidence files present. |
| `py -3 .aide/scripts/aide_lite.py contract-envelope status` | 0 | PASS | Reports `aide.dev/v1alpha1`. |
| `py -3 .aide/scripts/aide_lite.py contract-envelope project --source lifecycle-fixture-runner` | 0 | PASS | 3 projections written, no mutation claims. |
| `py -3 .aide/scripts/aide_lite.py contract-envelope validate` | 0 | PASS | Schema loaded, parsed, subset validation executed, alignment PASS. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-fixture status` | 0 | PASS | Capability remains `fixture_temp_apply_only`. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-fixture run --scenario install-managed-section --mode apply-temp` | 0 | PASS | Temp workspace mutation only. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-fixture verify` | 0 | PASS | 48 checks passed. |
| `py -3 .aide/scripts/aide_lite.py validate` | 0 | PASS | Repo validation passed. |
| `py -3 .aide/scripts/aide_lite.py test` | 0 | PASS | AIDE Lite test passed. |
| JSON parse checks | 0 | PASS | Schema, reports, projections, and lifecycle reports parsed. |
| PyYAML parse check | 2 | UNAVAILABLE | `yaml` module is not installed. |
| stdlib YAML structural check | 0 | PASS | Changed YAML files passed structural fallback checks. |
| overclaiming scan | 0 | PASS | No unsupported readiness/capability overclaims found. |
| broad secret marker scan | 1 | WARN_FALSE_POSITIVE | Existing helper-code marker strings in `aide_lite.py`; no secret value found. |

Result is `ACCEPTED_WITH_WARNINGS` because the remaining warnings are
environmental, known scan-noise, or explicitly deferred by design.
