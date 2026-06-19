# AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01

Build the first schema-only PatchTransaction protocol record.

Scope:

- model proposed mutation metadata and evidence;
- include base/source refs, diff/patch refs, allowed and forbidden paths,
  required capabilities, required conformance results, approvals, test
  requirements, evidence refs, rollback-compatible refs, quarantine state,
  idempotency key, and events;
- preserve accepted warning debt and explicit non-capabilities.

Non-goals:

- no apply engine;
- no target-repository mutation;
- no branch/worktree automation;
- no adapter execution;
- no runtime, Service, Test Broker, Commander, or Workbench;
- no provider/model/Gateway/network calls;
- no release or promotion behavior.

Stop at the appropriate build review gate.
