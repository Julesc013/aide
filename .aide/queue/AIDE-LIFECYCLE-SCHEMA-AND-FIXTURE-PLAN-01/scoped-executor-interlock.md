# Scoped Executor Interlock

Future lifecycle plans must compile to scoped transaction plans or compatible transaction bundles before any fixture proof can be considered.

## Required Mapping

- lifecycle plan `explicit_operations` maps to scoped transaction `operations`;
- lifecycle plan `explicit_paths` maps to scoped transaction target `path` values;
- lifecycle `allowed_roots` and `protected_roots` map directly to scoped transaction boundaries;
- lifecycle preimage hash requirements map to scoped transaction `expected_preimage_hash`;
- lifecycle postimage hash requirements map to scoped transaction `expected_postimage_hash`;
- lifecycle report destination maps to scoped transaction `report_path`;
- lifecycle rollback-compatible record destination maps to scoped transaction `rollback_record_path`;
- lifecycle `mode: report` and `mode: dry-run` map to scoped transaction report or dry-run mode;
- lifecycle fixture apply may map to scoped transaction `mode: apply` only after explicit future authorization.

## V0 Constraints

- Explicit paths only.
- Explicit operation allowlists.
- Managed-section operations by default.
- Preimage hash checks before mutation.
- Postimage verification after planned mutation.
- Staged-change and rollback-compatible records.
- Dry-run/report mode before apply.
- Multi-mutating apply remains blocked by scoped executor v0 unless a later reviewed capability changes it.
- Lifecycle fixture apply must respect the single-mutating-operation limit or split work into separately reviewed transactions.
- No target apply until target-local authority exists.

## Known Gaps

- Multi-file atomic apply is not implemented.
- Rollback execution is not implemented.
- Uninstall/delete safety is not implemented.
- Lifecycle pack manifest validation is not wired into AIDE Lite yet.
- Target repo adoption authority is not present.
- Active AIDE repo apply remains blocked pending a separate gate.

These gaps are not solved by this task.
