# Commands Run

## Starting Inspection

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short --branch` | PASS | `main...origin/main [ahead 1]` before checkpoint edits. |
| `git log --oneline -30` | PASS | Shows X-OS-02, X-OS-01, X-OS-00, AIDE-CONTINUE-00, and X-TEST-00 commits. |
| `git remote -v` | PASS | origin points to `https://github.com/Julesc013/aide.git`. |
| `git rev-parse HEAD` | PASS | `d5e3e818841931702cd4e2cde49452744afab985`. |
| `git rev-parse --show-toplevel` | PASS | `C:/Projects/AIDE/aide`. |
| `git tag --list` | PASS | no tags. |
| `git diff --check` | PASS | no whitespace errors. |

## Validation

| Command | Result | Notes |
| --- | --- | --- |
| `py -3 .aide/scripts/aide_lite.py doctor` | PASS | no hard validation failures. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | validation passed. |
| `py -3 .aide/scripts/aide_lite.py test` | PASS | canonical AIDE Lite test runner. |
| `py -3 .aide/scripts/aide_lite.py selftest` | PASS | internal checks passed. |
| `py -3 .aide/scripts/aide_lite.py eval run` | PASS | 158/158 golden tasks, 0 warnings, 0 failures. |
| post-artifact `doctor`, `validate`, `test`, `selftest`, `eval run` | PASS | rerun after checkpoint reports and latest task packet were written. |
| `py -3 .aide/scripts/aide_lite.py verify` | PASS | 89 checked files, 52 changed files, 0 warnings, 0 errors. |
| final `git diff --check` | PASS | no whitespace errors after evidence edits. |
| final targeted secret scan | PASS | no matches after excluding `secret-scan.md` to avoid the recorded pattern self-match. |
| `py -3 -m unittest discover -s .aide/scripts/tests` | PASS | 325 tests in 603.233 seconds. |
| `py -3 .aide/scripts/aide_lite.py test tiers` | PASS | T0-T3 reported. |
| `py -3 .aide/scripts/aide_lite.py test plan` | UNSUPPORTED | exact subcommand not exposed. |
| `py -3 .aide/scripts/aide_lite.py test tier-plan` | PASS | supported planner. |
| `py -3 .aide/scripts/aide_lite.py test impact-plan` | PASS | recommended T2 for diff from HEAD~1. |
| `py -3 .aide/scripts/aide_lite.py test telemetry-status` | PASS | no target test execution. |
| `py -3 .aide/scripts/aide_lite.py test summary-validate` | UNSUPPORTED_INPUT | requires `--file`. |
| `py -3 .aide/scripts/aide_lite.py test summary-validate --file .aide/tests/examples/test-summary.example.json` | PASS | example validates. |
| `py -3 .aide/scripts/aide_lite.py test full-discovery-handoff --reason ...` | PASS | external handoff only. |
| `py -3 .aide/scripts/aide_lite.py test slow-report-validate --file .aide/tests/examples/slow-test-report.example.json` | PASS | example validates. |

## Task OS And Capability Commands

All required Task OS and capability commands passed. Task OS commands remain report-only but generated checkpoint/next-plan reports are stale relative to X-OS-02 truth. Capability overclaim report passed with one non-blocking warning.

## Pack, Release, Lifecycle, Governance

| Command | Result | Notes |
| --- | --- | --- |
| `py -3 .aide/scripts/aide_lite.py pack-status` | PASS | checksums valid, boundary PASS, DIRTY_SOURCE_RECORDED. |
| `py -3 .aide/scripts/aide_lite.py release validate` | PASS | no publish, tag, GitHub release, or upload. |
| `py -3 .aide/scripts/aide_lite.py release draft-validate` | PASS | no publish, tag, upload, or network API call. |
| `py -3 .aide/scripts/aide_lite.py install validate` | PASS | no_apply true, target_mutation false. |
| `py -3 .aide/scripts/aide_lite.py repair validate` | PASS | no_apply true, target_mutation false. |
| `py -3 .aide/scripts/aide_lite.py upgrade validate` | PASS | no_apply true, target_mutation false. |
| `py -3 .aide/scripts/aide_lite.py rollback validate` | PASS | no_apply true, target_mutation false. |
| `py -3 .aide/scripts/aide_lite.py uninstall validate` | PASS | no_apply true, no blanket `.aide` deletion. |
| `py -3 .aide/scripts/aide_lite.py commit check --latest` | PASS | X-OS-02 commit message passes policy. |
| `py -3 .aide/scripts/aide_lite.py changelog preview` | PASS | preview-only, release publishing false, 13 malformed historic commits reported. |
| `py -3 .aide/scripts/aide_lite.py changelog validate` | PASS | preview outputs validate. |
| `py -3 .aide/scripts/aide_lite.py git plan` | BLOCKED_ADVISORY | dirty tree before checkpoint commit; dry_run true, no mutation. |
| `py -3 .aide/scripts/aide_lite.py pack --task "AIDE-FIX-OS-03 ..."` | PASS | latest task packet written; budget PASS; next task points to blocker repair. |
| post-pack `task status` | PASS_WITH_WARNING | report-only command passed; latest task parsing returned partial id `X-OS-03` instead of the canonical `AIDE-FIX-OS-03...` task id. |
