# Capability Negotiation

## Purpose

Capability negotiation is how AIDE keeps runtime feature claims aligned with researched lane ceilings, current implementation state, and the context a specific request can actually provide.

## Report identity

A capability report must identify:

- host family
- adapter technology
- support mode
- execution mode
- current capability
- target capability

These identities must use canonical inventory ids where applicable.

## Current versus target

- current capability is what AIDE has actually implemented and verified for that lane
- target capability is the planned honest ceiling derived from research and architecture intent

These are not the same thing.

## Feature availability

A capability report should declare:

- available features
- unavailable features
- reasons for unavailability

Typical reasons include:

- `not-implemented`
- `host-ceiling`
- `missing-context`
- `execution-mode-mismatch`
- `deferred`

## Negotiation flow

1. The adapter reports its lane identity and current local context.
2. The shared core evaluates the requested feature against capability requirements and available context.
3. The shared core returns availability or structured unavailability.
4. The adapter surfaces that result without inflating it into broader lane claims.

## Host ceiling versus AIDE state

Theoretical host ceiling and AIDE implementation state must remain separate.

Example:

- a host contract may theoretically support `L3`
- the lane may currently implement only `L1`
- a feature needing `L2` must still be reported unavailable today

This distinction is required for support honesty and for clean planning.
