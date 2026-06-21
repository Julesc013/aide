# Demo Operation Ledger Review

```json
{
  "allowed_operation_count": 6,
  "coverage": {
    "branch_worktree_ref_ops": false,
    "filesystem_writes": false,
    "git_reads": true,
    "mutation_apply": false,
    "network_attempts": false,
    "provider_model_attempts": false,
    "worker_dispatch": false
  },
  "forbidden_operation_count": 0,
  "injection_detected": true,
  "material_gaps": [
    "allowed_operation_count missing",
    "instrumentation coverage missing",
    "ledger does not describe every required operation family"
  ],
  "missing_field_entries": [],
  "operation_count": 6,
  "result": "REQUEST_CHANGES"
}
```
