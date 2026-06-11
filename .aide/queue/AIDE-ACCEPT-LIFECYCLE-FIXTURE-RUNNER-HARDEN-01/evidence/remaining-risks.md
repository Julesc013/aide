# Remaining Risks

Non-blocking risks:

- The accepted capability is intentionally limited to
  `install-managed-section` / `apply-temp` / `update_managed_section` against a
  temp fixture workspace.
- Formal public contract-envelope extraction remains future work.
- Broader conformance fixture coverage remains future work.

Deliberate deferrals:

- WorkUnit CLI, Test Broker, Codex adapter, Service, Commander, provider
  adapters, branch/worktree automation, target repo apply, active repo apply,
  rollback execution, uninstall execution, release, promotion, network,
  Gateway, GitHub mutation, and model/provider calls remain out of scope.
