# Recommended Next Work

Primary next task:

```text
AIDE-BUILD-CONTRACT-ENVELOPE-HARDEN-01
```

Reason:

The implementation is safe and passed validation, but the check result is
`PASS_WITH_WARNINGS` because the schema artifact is not wired into runtime
validation. This warning concerns schema/helper alignment, so hardening should
come before extracting the EvidencePacket schema.

Prompt seed:

```text
Create and process AIDE-BUILD-CONTRACT-ENVELOPE-HARDEN-01. Harden the reviewed
minimal contract envelope without widening authority. Focus only on validation
gaps, projection consistency, schema/helper alignment, unknown optional field
tolerance, unknown required capability fail-closed behavior, compatibility
checks, and clearer evidence. Do not build EvidencePacket schema, WorkUnit CLI,
Test Broker, Service, Commander, provider adapters, branch/worktree automation,
target repo apply, active repo apply, rollback execution, release, promotion,
network, Gateway, GitHub mutation, or model/provider calls. End at needs_review
with evidence.
```
