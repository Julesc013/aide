# Commands Run

| Command | Result | Notes |
|---|---:|---|
| `git status --short --branch` | PASS | Initial worktree clean on `main`. |
| `git remote -v` | PASS | `origin` is `https://github.com/Julesc013/aide.git`. |
| `git rev-parse --show-toplevel` | PASS | `C:/Projects/AIDE/aide`. |
| `git rev-parse HEAD` | PASS | `f2d536aad6de1b1a45cf91fb623f4f690c688c0d`. |
| `git log --oneline -20` | PASS | Latest commit `f2d536a feat(validation): add cross-repo test tier model`. |
| `git tag --list` | PASS | No tags listed. |
| `git diff --check` | PASS | No whitespace errors before scoped edits. |
| `py -3 .aide/scripts/aide_lite.py intent compile --prompt ...` | PASS | Wrote `.aide/intake/latest-*`; classified raw request as not directly executable and requiring bounded WorkUnit. |
| `py -3 .aide/scripts/aide_lite.py doctor` | PASS | Pre-edit doctor passed. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | Pre-edit validation passed. |
| `py -3 .aide/scripts/aide_lite.py task status` | PASS | Queue count increased to 58 and AIDE-CONTINUE-00 is indexed as `needs_review`. |
| `py -3 .aide/scripts/aide_lite.py test tiers` | PASS | T0 through T3 tier model present. |
| `py -3 .aide/scripts/aide_lite.py test telemetry-status` | PASS | Refreshed telemetry status for current source commit. |
| `py -3 .aide/scripts/aide_lite.py doctor` | WARN | Intermediate run reported validation should be run after dirty-tree edits; expected before final validation. |
| `py -3 .aide/scripts/aide_lite.py validate` | FAIL then PASS | First run failed because the refreshed task packet lacked required compact-task headings; packet was fixed and validation passed. |
| `py -3 .aide/scripts/aide_lite.py test` | PASS | Harness tests passed. |
| `py -3 .aide/scripts/aide_lite.py selftest` | PASS | Harness selftest passed. |
| `py -3 .aide/scripts/aide_lite.py pack-status` | PASS | Pack status reports `DIRTY_SOURCE_RECORDED`, boundary PASS, and checksums valid. |
| `py -3 .aide/scripts/aide_lite.py release validate` | PASS | Local bundle validation only; no publication. |
| `py -3 .aide/scripts/aide_lite.py release draft-validate` | PASS | Draft validation only; no tag, upload, or release publication. |
| `py -3 .aide/scripts/aide_lite.py install validate` | PASS | No-apply install boundary validated. |
| `py -3 .aide/scripts/aide_lite.py repair validate` | PASS | No-apply repair boundary validated. |
| `py -3 .aide/scripts/aide_lite.py upgrade validate` | PASS | No-apply upgrade boundary validated. |
| `py -3 .aide/scripts/aide_lite.py rollback validate` | PASS | No-apply rollback boundary validated. |
| `py -3 .aide/scripts/aide_lite.py uninstall validate` | PASS | No-apply uninstall boundary validated; blanket `.aide` deletion remains false. |
| `py -3 .aide/scripts/aide_lite.py eval run` | PASS | 140 golden tasks passed; no provider/model calls, network calls, raw prompt storage, or raw response storage. |
| `py -3 .aide/scripts/aide_lite.py git plan` | WARN | Report-only plan wrote `.aide/git/latest-*` and blocked on the expected dirty tree. |
| `py -3 .aide/scripts/aide_lite.py intent validate` | PASS | Intent policy, schema, and latest intake packet validated. |
| `py -3 scripts/aide validate` | PASS_WITH_WARNINGS | Structural validation passed with the pre-existing generated-source stale fingerprint warning. |
| Targeted credential scan over changed paths | PASS | Value-shaped credential scan returned `NO_MATCHES`; broader name scans had documentation/path false positives on `task-os` and the secret-scan evidence text itself. |
| `git diff --check` | PASS | Final pre-commit whitespace check passed. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | Final pre-commit AIDE Lite validation passed. |
| `py -3 .aide/scripts/aide_lite.py doctor` | PASS | Final pre-commit doctor passed; no hard validation failures detected. |
| `py -3 .aide/scripts/aide_lite.py task status` | PASS | Final pre-commit task status includes AIDE-CONTINUE-00 as `needs_review` and `implemented`. |
