# Remaining Risks

- PatchTransaction acceptance is blocked until the path-scope fail-closed
  defects are repaired and independently rechecked.
- The minimal slice remains schema/projection/validation only, with no apply,
  approval, policy, admission, trust, rollback, event store, runtime, worker, or
  provider behavior.
- Existing operational-health warning debt remains unresolved and was not in
  scope for this check.
