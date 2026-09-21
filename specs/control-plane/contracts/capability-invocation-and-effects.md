# Capability Invocation and Effects

| Field | Value |
|---|---|
| Contract status | Adopted desired-state contract |
| Source family | S21 capability and effect contract, adapted to live AIDE boundaries |
| Implementation | Partial and binding-specific |
| Behavioral qualification | Not established by this document |
| Owner | Capability owner and provider within delegated authority |

## Principle

AIDE separates four related records:

1. A capability definition describes typed inputs, outputs, domain meaning,
   effect families, determinism, cancellation, and limitations.
2. A binding identifies the exact implementation, command vector, environment,
   dependencies, decoder, and qualification subject.
3. An invocation binds a capability and binding to an actor, subject, source
   revision, authority, deadline, and resource reservation.
4. A receipt records observed outcomes and effects for that invocation.

A provider-supplied success value or process exit code is not sufficient proof
of domain success. Receipt axes follow the separate outcomes defined in
[Status and outcome dimensions](status-and-outcome-dimensions.md).

This contract does not enable a provider, network path, tool, shell, or target
mutation. Applicable policy and an admitted WorkUnit still control execution.

## Effect Boundaries

Read-only is an effect classification, not an informal tool label. A validator
that writes a contained cache or report must declare that output separately
from source mutation. Capabilities must distinguish filesystem, process,
network, secret, storage, billing, integration, and publication effects where
they differ.

Project adapters retain native commands, domain results, and refusal semantics.
Generic providers may supply bounded launch, capture, custody, and receipt
mechanics, but they must not replace project-native acceptance rules. Fixed,
registered command contracts are preferred over arbitrary shell text.

## Requirements

### AIDE-CAP-001: Exact Binding Coherence

An invocation MUST match its admitted capability, provider, command, input
schema, and binding digest before launch.

### AIDE-CAP-002: Effect Catalogue

Capabilities MUST declare supported and unsupported read, write, network,
secret, process, storage, billing, integration, and publication effects that
apply to their operation.

### AIDE-CAP-003: Per-Invocation Accounting

Receipts MUST record launch counts, identities, resource use, and effects for
the individual invocation rather than cumulative provider-object state.

### AIDE-CAP-004: Fail-Closed Decoding

Malformed output, failed probes, or incomplete custody MUST leave affected
domain, verification, and evidence axes incomplete or failed.

### AIDE-CAP-005: Native Authority

Adapters MUST preserve project-native validators and refusal semantics instead
of reimplementing domain acceptance in AIDE.

### AIDE-CAP-006: Literal Command Contracts

External commands MUST use explicit argument vectors, a controlled environment,
and bounded outputs without shell interpolation by default.

### AIDE-CAP-007: Truthful Cancellation

Each binding MUST state whether local cancellation, descendant termination,
remote cancellation, and billing cessation are implemented and qualified.

## Acceptance Direction

Acceptance should cover mismatched provider bindings, contained writes from a
nominally read-only capability, repeated provider use, decoder failure after
process success, native domain refusal, shell metacharacters in data, and local
disconnect where remote cancellation is unavailable.

These are desired acceptance cases. This document records none of them as run.
