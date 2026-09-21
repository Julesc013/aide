# AIDE Control-Plane Specifications

This area contains adopted desired-state contracts and explicitly labelled
draft design chapters for AIDE as a repo-native development control plane. It extends the preserved shared-core and host
architecture; it does not restart the product or replace `.aide/` as the
self-hosting contract and queue.

## Status Vocabulary

Every contract should distinguish these dimensions when they matter:

| Dimension | Question |
|---|---|
| Adoption | Has the desired behavior been reviewed as an AIDE contract? |
| Implementation | Does source implement the contract for an identified profile? |
| Verification | Which exact tests or observations passed, failed, or were not run? |
| Activation | Is the behavior enabled for the current repository or target? |
| Support | Which exact release and environment receive a maintained promise? |

An adopted contract may remain unimplemented. A working prototype may remain
unqualified or unsupported. No single percentage or `PASS` value replaces
these facts.

## Adopted Foundation

### Product

- [Product scope and profiles](product/scope-and-profiles.md)

### Contracts

- [Authority and decision provenance](contracts/authority-and-decision-provenance.md)
- [Status and outcome dimensions](contracts/status-and-outcome-dimensions.md)
- [WorkUnits, attempts, and decomposition](contracts/work-attempts-and-decomposition.md)
- [Capability invocation and effects](contracts/capability-invocation-and-effects.md)
- [Identity, references, and digests](contracts/identity-references-and-digests.md)

## Preserved Related Contracts

- [Shared-core and host architecture](../architecture/README.md)
- [Accepted shared-core ADR](../architecture/adr/ADR-0001-shared-core-many-hosts.md)
- [Boot-slice baseline](../boot-slice/README.md)

## Imported Draft Design Chapters

The earlier generated design is now available in its intended directories.
[Draft chapter index and source identities](draft-import.md) lists the 34
imported chapters, alongside the six adopted foundation contracts above.

These drafts cover compatibility, execution bindings, trust, engineering,
recovery, lifecycle, knowledge, optimization, interoperability, and operator
experience. They retain proposed requirements and unrun acceptance designs;
copying the files does not adopt those requirements or enable the behavior.
Existing adopted contracts retain precedence. Candidate bulk registers and
private archive material remain external review inputs.

## Operational Boundary

These documents do not grant tool access, mutation, spending, integration,
publication, or release authority. Current policy, queue scope, actor authority,
and exact review gates still decide whether an operation may occur.
