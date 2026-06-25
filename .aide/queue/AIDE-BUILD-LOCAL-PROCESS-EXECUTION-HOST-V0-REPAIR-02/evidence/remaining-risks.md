# Remaining Risks

- This is still a deterministic fixture-backed reference host, not a general
  local worker harness.
- Public cancellation remains unsupported in v0.
- Durable idempotency, process supervision, process-tree cancellation, resource
  quotas, streaming artifact storage, Service runtime, Workbench runtime,
  provider/model/network execution, preview/apply/rollback, and repository
  mutation remain non-capabilities.
- Reparse-point fixture coverage depends on platform support; implementation
  checks are present, but no cross-platform claim is made.
