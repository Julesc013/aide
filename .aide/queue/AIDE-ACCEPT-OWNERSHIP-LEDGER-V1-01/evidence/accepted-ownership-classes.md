# Accepted Ownership Classes

Accepted capability: `ownership_ledger_v1`

The accepted taxonomy contains eleven classes:

- `vendor_managed_file`: AIDE-distributed file with exact source digest authority.
- `vendor_managed_section`: AIDE-distributed managed section inside a host file.
- `project_owned`: target project file that AIDE must not overwrite silently.
- `project_overlay`: target-owned overlay that configures an AIDE distribution.
- `project_generated`: target-local generated projection recreated in target context.
- `runtime_generated`: runtime or local generated state outside committed distribution truth.
- `local_only`: local operator state that is never distribution truth.
- `evidence_only`: audit evidence, not source distribution content.
- `preserved_legacy`: legacy or pre-existing target state preserved unless manually migrated.
- `unknown`: insufficient ownership proof; blocks automatic apply.
- `never_touch`: path class that distribution apply must never modify.

All classes record `automatic_apply_allowed: false`.
