# Guard Exercise Review

The check invoked the actual guard dispatcher with nonce-bearing requests and
sentinel executors.

- probe_count: `6`
- passed_count: `6`
- failed_count: `0`

Families exercised:

- `filesystem_writes`
- `branch_worktree_ref_ops`
- `network_attempts`
- `provider_model_attempts`
- `worker_dispatch`
- `mutation_apply`

Every probe reached the guard, preserved state, returned a typed refusal, and
left the sentinel executor uncalled.
