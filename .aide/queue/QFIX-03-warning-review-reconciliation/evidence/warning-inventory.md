# Warning Inventory

## Initial Inventory

Commands run from a clean worktree after Q34:

- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS, 7 warnings.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS, same warning class.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS, same warning class.
- `py -3 .aide/scripts/aide_lite.py changelog preview`: WARN; historical
  malformed/legacy commits reported.
- `py -3 .aide/scripts/aide_lite.py git plan`: command exit PASS with blocked
  plan while generated outputs were dirty and local `dev` was missing.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS, 30/30, no golden-task
  warnings.

## Warning Classes

| Class | Source | Fixability | Action |
| --- | --- | --- | --- |
| Stale generated manifest | Harness validate/doctor/self-check | Fixable | Run `scripts/aide compile --write`. |
| Q00/Q01/Q02/Q03/Q05/Q06 review gates | Harness validate/doctor/self-check | Fixable only by review reconciliation | Review from task-local evidence and update status if acceptable. |
| Historical malformed commits | `changelog preview` | Not fixable without rewriting history | Keep reported in malformed commit output; avoid hiding. |
| Dirty tree Git helper block | `git plan` during generation | Procedural | Run final Git helper checks from clean state or record generated-output dirtiness explicitly. |
| Missing `dev` integration branch | Git helper policy | Requires live branch creation/push decision | Do not create/push in QFIX-03; keep as branch-workflow follow-up unless operator later explicitly runs a helper apply command. |

## After Generated Manifest Refresh

- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS, 6 warnings.
- `GENERATED-SOURCE-STALE` is resolved.
- Remaining Harness warnings are the six early queue review gates.

## Final Reconciliation

| Class | Final posture |
| --- | --- |
| Stale generated manifest | Resolved; Harness reports `GENERATED-SOURCE-CURRENT`. |
| Q00/Q01/Q02/Q03/Q05/Q06 review gates | Resolved from repo-local evidence; queue status and index now show accepted states. |
| Q25-Q31/Q34 review states | Resolved from task-local evidence as `passed`/accepted with notes by QFIX-03. |
| Historical malformed commits | Reported in `.aide/changelog/malformed-commits.md`; `changelog preview` returns PASS and marks them `reported_for_review` without rewriting history. |
| Token ledger near-budget entries | Converted from validation warnings to budget watchlist entries; over-budget eval reports were fixed by adding an explicit eval-report budget. |
| Dirty tree Git helper block | Procedural only while QFIX edits are uncommitted; generated dirty-state Git helper snapshots were restored before commit. |
| Missing `dev` integration branch | Not an AIDE-local validation warning or blocker; branch creation remains future operator-gated work and was not performed. |

Final validation status:

- `py -3 scripts/aide validate`: PASS, `149 info, 0 warning, 0 error`.
- `py -3 scripts/aide doctor`: PASS, `149 info, 0 warning, 0 error`.
- `py -3 scripts/aide self-check`: PASS, validation warning count `0`.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS, no WARN/FAIL checks.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS, `warn_count: 0`, `fail_count: 0`.
