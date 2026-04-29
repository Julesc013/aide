# ADR-0007: Hosts Are Shells

## Status

accepted

## Context

Bootstrap-era host lanes contain important proofs and blockers. The reboot needs to preserve those records while preventing host-specific shells from owning durable semantics.

## Decision

AIDE Hosts are shells, adapters, and proof lanes. Durable semantics belong in AIDE Core contracts and are mediated through Harness, Compatibility, Control, SDK, Runtime, and Bridges as appropriate.

## Consequences

- Host-lane implementation must consume Core contracts.
- Host-specific capabilities remain honest through Compatibility.
- Future IDE Hosts are deferred until the queue authorizes them.

## Supersedes / Superseded By

Supersedes: none. Superseded by: none.
