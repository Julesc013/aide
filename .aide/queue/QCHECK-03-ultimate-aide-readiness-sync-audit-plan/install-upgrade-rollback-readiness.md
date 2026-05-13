# Install, Upgrade, Repair, Rollback, and Uninstall Readiness

## Existing

- Portable pack generation.
- Pack checksums and boundary validation.
- Safe import dry-run behavior.
- Target-specific placeholder templates.
- Commit/task/git/changelog governance included in pack.
- Hook template present but not auto-installed.
- Target Q32/Q33 evidence shows targeted sync can preserve target state.

## Missing

| Capability | Current status | Required next artifact |
|---|---|---|
| observe | partial via dry-run/import inspection | install preflight schema |
| plan | partial via dry-run output | install plan schema |
| apply | unsafe for broad use | explicit apply command with ownership ledger |
| verify | partial via AIDE Lite validation | install verification report schema |
| repair | missing | repair plan and safe file reconstruction policy |
| upgrade | missing | upgrade plan with compatibility checks |
| rollback | missing | rollback manifest and restoration procedure |
| uninstall | missing | uninstall plan that preserves target state |
| release bundle | missing | stable pack release bundle manifest |
| GitHub release draft | missing | preview-only release draft command |

## Safety Requirements

- Dry-run first.
- No target product roots by default.
- No target manual content overwrite without explicit conflict resolution.
- No hook auto-install.
- No branch mutation.
- No source repo queue/history/context/report state copied.
- Reversible changes only until target review accepts apply.

## Verdict

AIDE Lite Pack is installable only by controlled targeted sync or safe dry-run
today. It is not yet the "ultimate stable installer" until Q43-Q48 exist.
