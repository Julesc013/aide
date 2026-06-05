# Validation

## Preflight Commands

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short --branch` | PASS | Preflight output: `## main...origin/main`. |
| `git remote -v` | PASS | `origin` fetch/push remote present. |
| `git rev-parse HEAD` | PASS | Initial HEAD `a6d12bd62a4112e784708847c1b12356f2c29e4d`. |
| `git show --stat --oneline --name-status HEAD` | PASS | Materialization commit inspected; 87 files changed. |
| `git diff --check HEAD^ HEAD` | PASS | No whitespace errors in upstream materialization commit. |
| `py -3 .aide/scripts/aide_lite.py task --help` | PASS | Task subcommands available. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema --help` | PASS | `status`, `validate`, and `fixture-verify` available. |
| `py -3 .aide/scripts/aide_lite.py task status` | PASS | 79 tasks before checkpoint index addition; materialization was latest. |
| `py -3 .aide/scripts/aide_lite.py task next-plan` | PASS_WITH_WARNINGS | Global next-plan selected `AIDE-APPLY-LIFECYCLE-PLAN-01`; task-local next batch selected this checkpoint. |
| `py -3 .aide/scripts/aide_lite.py task inspect AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01` | NOT_RUN | Positional form is unsupported by the CLI and rejected arguments. |
| `py -3 .aide/scripts/aide_lite.py task evidence AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01` | NOT_RUN | Positional form is unsupported by the CLI and rejected arguments. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01` | PASS | Upstream status `needs_review`, classification `complete`, evidence files 9, missing 0. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01` | PASS | Upstream evidence files listed; missing none. |

## Final Validation Commands

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short --branch` | PASS_WITH_EXPECTED_CHANGES | Checkpoint queue files, latest packet, queue index, and deterministic generated report refreshes present. |
| `git diff --check` | PASS | No output. |
| `git diff --cached --check` | PASS | No staged changes at time of check; no output. |
| `git diff --check HEAD^ HEAD` | PASS | No whitespace errors in upstream materialization commit; no output. |
| `py -3 .aide/scripts/aide_lite.py task status` | PASS | 80 tasks after checkpoint index addition; latest task `AIDE-LIFECYCLE-FIXTURE-CHECK-01`. |
| `py -3 .aide/scripts/aide_lite.py task next-plan` | PASS_WITH_WARNINGS | Still selects global next WorkUnit `AIDE-APPLY-LIFECYCLE-PLAN-01`; checkpoint-local next batch selects `AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01`. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-CHECK-01` | PASS | Status `needs_review`, classification `complete`, evidence files 11, missing 0. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-CHECK-01` | PASS | 11 checkpoint evidence files listed, missing none. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01` | PASS | Upstream remains `needs_review`, complete, evidence files 9, missing 0. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01` | PASS | Upstream evidence files listed, missing none. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | Latest task packet tokens `1366`; no token warning after trim. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema status` | PASS_WITH_NOTES | Report-only; lifecycle apply false; physical fixture tree materialization is outside this validator's status flag. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema validate` | PASS | 280 checks. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema fixture-verify` | PASS | 298 checks, shape-only. |
| `py -3 .aide/scripts/aide_lite.py scoped-transaction status` | PASS | Report-only; target mutation false; branch mutation false; provider/model/Gateway/network none. |
| `py -3 .aide/scripts/aide_lite.py managed-section status` | PASS | Report-only; active repo apply false; target mutation false. |
| `py -3 .aide/scripts/aide_lite.py transaction status` | PASS | Report-only; real repo apply false; target mutation false. |

## Independent Fixture Review

Corrected read-only parse/hash review:

```json
{
  "result": "PASS",
  "changed_files_checked": 37,
  "json_checked": 3,
  "yaml_structural_checked": 3,
  "scenario_count": 13,
  "expected_report_count": 7,
  "rollback_record_count": 2,
  "indexed_hash_records": 11,
  "errors": []
}
```

The script parsed changed JSON/YAML-like files, fixture index, scenario metadata, expected reports, rollback records, and recomputed indexed SHA-256 hashes. An earlier attempt failed because it treated repo-relative fixture index paths as fixture-relative paths; the corrected run passed and is the recorded result.

## Boundary Text Search

Command: `rg -n -i -F` over changed files plus reviewed fixture/materialization paths for required boundary terms.

Result: PASS. Required forbidden-operation and capability terms were found in checkpoint/materialization/fixture evidence as prohibitions, non-goals, false flags, blocked examples, or review-gated labels, including install apply, upgrade apply, lifecycle repair apply, rollback/uninstall, lifecycle apply execution, scoped transaction apply against fixture targets, active repo scoped apply mutation, target repo mutation, branch/worktree mutation, merge, push, promotion, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, broad active-repo apply, production-ready, release-ready, and `needs_review`.

## Secret Scan

Command: `rg -n -i -e "SECRET|TOKEN|API_KEY|PRIVATE_KEY|PASSWORD|GITHUB_TOKEN|OPENAI_API_KEY|ANTHROPIC_API_KEY|AWS_ACCESS_KEY|AWS_SECRET_ACCESS_KEY"` over changed files plus reviewed fixture/materialization paths.

Result: PASS_WITH_WARNINGS. Scanned 106 files with 47 marker hits. Hits were protected-path metadata, token-budget/task-name words, and fixture examples such as `secrets/example.env`; no credential material was found.

## Generated Report Churn

Required status and validation commands refreshed deterministic generated reports under `.aide/reports/**`. Those changes are retained as checkpoint evidence under the task allowlist.
