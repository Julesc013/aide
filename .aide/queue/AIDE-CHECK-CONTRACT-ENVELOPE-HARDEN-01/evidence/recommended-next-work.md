# Recommended Next Work

Primary next task:

```text
AIDE-ACCEPT-CONTRACT-ENVELOPE-01
```

Reason:

The hardening check passed with only a non-blocking environment warning for
PyYAML unavailability. Schema runtime truthfulness, helper/schema alignment,
compatibility, fail-closed behavior, projection correctness, tests, validation,
no-overclaiming, and forbidden operation boundaries were verified.

Prompt seed:

```text
Create and process AIDE-ACCEPT-CONTRACT-ENVELOPE-01. Perform acceptance review for the minimal contract envelope slice after BUILD, CHECK, HARDEN, and HARDEN-CHECK. Verify the accepted capability remains only the minimal envelope/projection/validation capability; verify schema runtime loading, minimal schema subset validation, helper/schema alignment, backward compatibility with lifecycle fixture reports, additive projections, unknown optional field tolerance, unknown required capability fail-closed behavior, reports, tests, validation, no destructive migration, no overclaiming, and forbidden operation preservation. Do not build EvidencePacket schema, WorkUnit schema, WorkUnit CLI, TestJob schema, Test Broker, Service, Commander, provider adapters, branch/worktree automation, target repo apply, active repo apply, rollback execution, release, promotion, network, Gateway, GitHub mutation, or model/provider calls. End with ACCEPTED, ACCEPTED_WITH_WARNINGS, REJECTED_NEEDS_REPAIR, BLOCKED, or PARTIAL and concrete next-task guidance.
```
