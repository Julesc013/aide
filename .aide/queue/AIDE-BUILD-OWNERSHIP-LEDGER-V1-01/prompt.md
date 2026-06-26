# AIDE-BUILD-OWNERSHIP-LEDGER-V1-01

Build proposed `ownership_ledger_v1` after accepted `project_lock_v0`.

Define ownership taxonomy and ledger records for:

- `vendor_managed_file`
- `vendor_managed_section`
- `project_owned`
- `project_overlay`
- `project_generated`
- `runtime_generated`
- `local_only`
- `evidence_only`
- `preserved_legacy`
- `unknown`
- `never_touch`

Do not implement install/update/apply behavior, target mutation, release
publication, network/provider calls, Workbench/MCP runtime, InstallRecord,
UpdatePlan, or downstream apply objects.

Stop at `needs_review` and recommend exactly:

```text
AIDE-CHECK-OWNERSHIP-LEDGER-V1-01
```
