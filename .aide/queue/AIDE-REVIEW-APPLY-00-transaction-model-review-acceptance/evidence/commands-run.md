# Commands Run

## Preflight

- `git status --short --branch` - PASS; branch `main`, dirty only after report-only task status refresh.
- `git log --oneline -30` - PASS.
- `git remote -v` - PASS; origin is `https://github.com/Julesc013/aide.git`.
- `git rev-parse HEAD` - PASS; `4fdf2e2e1d44f6d95ba528a63816a0619fbf6e8f`.
- `git rev-parse --show-toplevel` - PASS; `C:/Projects/AIDE/aide`.
- `git tag --list` - PASS; no tags.
- `git diff --check` - PASS.
- `py -3 .aide/scripts/aide_lite.py task status` - PASS; report-only.
- `py -3 .aide/scripts/aide_lite.py intent compile --prompt "...AIDE-REVIEW-APPLY-00..."` - PASS; risk_class governance, requires_split true.
- `py -3 .aide/scripts/aide_lite.py git plan` - report-only, blocked by dirty_tree_requires_classification after generated preflight reports; no branch/worktree/push/remote mutation.

## Search

- Broad contradiction search - PASS; matches were boundary/proof prose and expected no-apply language.
- Targeted forbidden marker search - PASS_WITH_NOTES; initial command had PowerShell regex quoting failure, corrected search found only proof statements and forbidden-string validation checks.

## Final Validation

See `validation.md`.

## Additional State Checks

- `py -3 scripts/aide validate` - PASS_WITH_WARNINGS; known generated-manifest stale warning.
- `py -3 .aide/scripts/aide_lite.py task status` - PASS; task_count 66, latest_task_id AIDE-APPLY-01.
- `py -3 .aide/scripts/aide_lite.py commit check --latest` - PASS for current pre-commit HEAD.
- `py -3 .aide/scripts/aide_lite.py commit check --message` - PASS for planned structured commit message.
