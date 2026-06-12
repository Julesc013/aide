# Next Task Recommendation

Primary next task:

```text
AIDE-BUILD-WORKUNIT-QUEUE-V1-01
```

Reason:

- Contract envelope is accepted.
- EvidencePacket trust-record shape is accepted with warnings.
- The next protocol-shaped vertical slice should define the minimal queue WorkUnit object.

Prompt seed:

```text
Create and process AIDE-BUILD-WORKUNIT-QUEUE-V1-01. Define the minimal queue WorkUnit object using the accepted contract envelope and EvidencePacket shapes. Keep scope narrow: queue WorkUnit identity, metadata, status, allowed/forbidden paths, dependencies, validation commands, evidence requirements, explicit non-capabilities, compatibility metadata, and additive projections/validation for existing queue tasks. Do not build WorkUnit CLI yet, TestJob schema, Test Broker, Service, Commander, provider adapters, branch/worktree automation, target repo apply, active repo apply, rollback execution, release, promotion, network, Gateway, GitHub mutation, or model/provider calls. End at needs_review with evidence.
```
