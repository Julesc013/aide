# ADR-0001: Shared Core, Many Hosts

## Status

Accepted

## Context

AIDE is intended to span multiple host families and multiple extension-technology lanes, including modern native lanes, legacy-native lanes, and companion lanes. The research corpus already shows that these hosts differ sharply in lifecycle, runtime constraints, native depth, and packaging rules.

At the same time, the repository also shows repeated cross-host needs:

- stable feature identification
- settings and overrides
- diagnostics
- capability reporting
- request and response handling
- reusable transforms and output shapes

The architecture therefore needed a stable answer to whether AIDE should be built as many separate products or as one shared system with multiple adapters.

## Decision

AIDE will use one shared core and many host adapters.

- the shared core owns reusable product behavior, protocol contracts, settings resolution, diagnostics behavior, capability negotiation, and cross-host transforms
- host adapters remain thin translation layers over host-specific SDKs, extension points, companion hooks, and packaging/runtime constraints
- execution may vary by lane through `embedded`, `cli-bridge`, or `local-service`, but the core request and response contracts remain stable

## Consequences

- later implementation prompts can build reusable behavior once instead of re-implementing it per host
- host adapters stay explicit about their real ceilings and host quirks
- capability negotiation becomes a first-class contract instead of an ad hoc implementation detail
- transport and packaging differences remain outside the shared product logic

## Alternatives considered

### Per-host isolated products

Rejected because it would duplicate feature semantics, diagnostics, and settings logic across lanes and make cross-host support honesty harder to maintain.

### One monolithic in-process runtime only

Rejected because the researched hosts do not share one safe or realistic execution strategy.

### Companion-only architecture

Rejected because some researched host families have meaningful native surfaces, and the project doctrine explicitly allows many host adapters rather than one external-only tool.
