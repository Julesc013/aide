# Scoped Executor Interlock

Result: `PASS_WITH_NOTES`

Every generated plan includes:

- `compatible_future_plan_class=fixture_dry_run_or_report_only`
- `apply_mode_authorized=false`
- v0 limitations for no multi-file lifecycle apply execution, no rollback execution, no uninstall/delete execution, and no target repo authority.

The interlock is sufficient for checkpoint acceptance because it prevents interpreting generated lifecycle plans as scoped transaction apply authority.

Limitations remain:

- No lifecycle apply execution is authorized.
- No scoped transaction apply against fixture targets is authorized.
- Multi-mutating lifecycle apply remains out of scope for scoped executor v0.
- Rollback execution remains out of scope.
- Uninstall/delete execution remains out of scope.
- Active repo and target repo authority remain blocked.
