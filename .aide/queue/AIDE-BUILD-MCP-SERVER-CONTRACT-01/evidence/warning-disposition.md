# Warning Disposition

Result classification: `PASS_WITH_WARNINGS`.

Warnings retained as non-blocking:

- MCP server contract is projection-only; no live MCP server or transport exists.
- Resources, prompts, and tools are catalogued and fixture-backed only; they are
  not served or callable.
- Authorization expectations are declared, but OAuth, credentials,
  `PolicyDecision`, and `CapabilityGrant` enforcement are not implemented.
- The preferred future `aide://interop/...` ReferenceID kind is advisory only;
  ReferenceID authority was not broadened.
- Inherited Interop Exports preview-only limitations and prior report, OKF, and
  Reconciler warning debt remain unresolved.

No warning invalidates MCP contract identity, fixture integrity, source
authority, or predecessor acceptance.
