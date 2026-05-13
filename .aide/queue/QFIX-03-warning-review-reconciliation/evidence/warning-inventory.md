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
