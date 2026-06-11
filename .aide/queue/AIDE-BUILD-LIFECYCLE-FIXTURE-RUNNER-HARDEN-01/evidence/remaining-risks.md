# Remaining Risks

Non-blocking remaining risks:

- The runner is still intentionally limited to `install-managed-section` /
  `apply-temp`.
- Broader conformance fixtures for many scenarios remain future work.
- This hardening validates report shape procedurally inside the runner; it does
  not introduce a formal public schema suite.

Deliberate deferrals:

- WorkUnit CLI, Test Broker, Codex adapter, Service, Commander, provider
  adapters, branch/worktree automation, target repo apply, active repo apply,
  rollback execution, uninstall execution, release, promotion, network,
  Gateway, GitHub mutation, and model/provider calls remain out of scope.
