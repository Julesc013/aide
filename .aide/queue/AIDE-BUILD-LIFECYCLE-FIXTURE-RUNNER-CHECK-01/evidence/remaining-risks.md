# Remaining Risks

## Non-Blocking Warnings

- Unsupported operation rejection exists in `ScopedExecutor.apply`, but the
  focused tests do not directly exercise that helper path.
- Malformed marker, duplicate marker, nested marker, malformed report, and
  broader conformance edge cases need more direct hardening tests.

## Deliberate Deferrals

- No implementation hardening was performed in CHECK-01 because this is a
  check-only task.
- No WorkUnit CLI, Test Broker, Codex adapter, Service, Commander,
  branch/worktree automation, target repo apply, active repo apply, rollback
  execution, uninstall execution, release, promotion, network, Gateway, GitHub
  mutation, or model/provider call work is authorized before this independent
  check reaches `needs_review`.

## Next Mitigation

Run `AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-HARDEN-01`.
