# Dominium Seam Plan

The cross-repo seam should be explicit before Workbench implementation grows.

The first seam task should be:

```text
AIDE-DOMINIUM-INTEGRATION-CHARTER-01
```

It should define:

- object ownership;
- namespace ownership;
- canonical status mapping;
- transaction composition;
- evidence mapping;
- capability negotiation;
- version compatibility;
- refusal behavior;
- source-of-truth hierarchy.

The first useful integration slice should avoid scene mutation and broad GUI
work. It should prove validation through existing deterministic paths:

```text
ContextDescriptor
-> ContextPack
-> WorkUnit
-> dominium.validation.run
-> typed result/refusal/evidence
-> EvidencePacket/EventRecord refs
-> Workbench or static projection summary
```

This validates Host Contract, Dominium Bridge mapping, WorkUnit correlation,
registered command invocation, typed refusal handling, evidence mapping, and
read-only projection without requiring Service, provider calls, dynamic modules,
scene mutation, or target repository apply.
