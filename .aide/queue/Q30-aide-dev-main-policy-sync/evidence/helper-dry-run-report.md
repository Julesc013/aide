# Q30 Helper Dry-Run Report

## Generated Plans

- `.aide/git/aide-dev-main-plan.json`
- `.aide/git/aide-dev-main-plan.md`
- `.aide/git/latest-helper-plan.json`
- `.aide/git/latest-helper-plan.md`

## Command Results

| Command | Result | Notes |
| --- | --- | --- |
| `py -3 .aide/scripts/aide_lite.py git detect` | PASS | Detected `trunk_without_dev`, current branch `main`, role `canonical`, non-mutating. |
| `py -3 .aide/scripts/aide_lite.py git doctor` | PASS | Reports AIDE branch policy present; warns on dirty tree and missing `dev`. |
| `py -3 .aide/scripts/aide_lite.py git status` | PASS | Reports `main` as canonical and `dev` as integration target. |
| `py -3 .aide/scripts/aide_lite.py git policy` | PASS | Validates Q28/Q29/Q30 policy anchors. |
| `py -3 .aide/scripts/aide_lite.py git plan` | PASS_BLOCKED | Blocks on dirty tree classification; warns `dev` missing; no mutation. |
| `py -3 .aide/scripts/aide_lite.py git sync --dry-run` | PASS_BLOCKED | Would inspect status and use ff-only pull if explicitly applied later; no fetch/pull/push run. |
| `py -3 .aide/scripts/aide_lite.py git land --dry-run --target dev` | PASS_BLOCKED | Blocks because source is protected canonical `main`, dirty tree exists, and target `dev` is missing. |
| `py -3 .aide/scripts/aide_lite.py git promote --dry-run --from dev --to main` | PASS_BLOCKED | Blocks because source `dev` is missing and dirty tree exists. |
| `py -3 .aide/scripts/aide_lite.py git prune --dry-run` | PASS | Only current/protected `main` observed; not eligible for prune. |

## Future Explicit Operator Plan

If a future reviewed task authorizes live `dev` setup, the generated Q30 plan
records these commands as not run:

```powershell
git switch -c dev main
git push -u origin dev
```

They require operator approval and validation before use.

## No-Mutation Confirmation

All helper runs used dry-run/report-only behavior. `--apply` and `--push` were
not run.
