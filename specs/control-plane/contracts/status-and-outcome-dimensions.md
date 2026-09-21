# Status and Outcome Dimensions

| Field | Value |
|---|---|
| Contract status | Adopted desired-state foundation |
| Source family | S21 status contract, adapted to live AIDE records |
| Implementation | Partial; existing schemas retain historical fields |
| Behavioral qualification | Not established by this document |
| Owner | Capability and status projections |

## Principle

A contract may exist without an implementation. A fixture may pass while a host
remains operationally unqualified. A mechanism may pass source review without
being installed or activated. These are separate facts, not caveats to hide in
one overloaded `PASS` value.

## Required Dimensions

Status projections MUST keep the following dimensions separate where relevant:

- lifecycle;
- specification adoption;
- implementation maturity;
- verification result;
- review and acceptance;
- operational activation;
- support tier and capability level;
- completeness against a named profile;
- effect certainty;
- warnings, expiry, and revocation conditions.

Existing queue values such as `planned`, `running`, `needs_review`, `passed`,
and `blocked` remain valid historical data. This contract does not silently
migrate their schemas.

## Outcome Axes

For an attempted operation, AIDE SHOULD distinguish:

1. Process outcome: did the executable run and exit?
2. Transport outcome: did communication complete?
3. Parsing outcome: was the response understood?
4. Domain outcome: did the requested work succeed, refuse, or fail?
5. Verification outcome: did an independent oracle confirm the result?
6. Integration outcome: did the authoritative destination accept the exact candidate?

Success on one axis does not imply success on another.

## Requirements

### AIDE-STATE-001: Orthogonal Status

AIDE MUST separately represent contract presence, implementation, verification,
acceptance, activation, and support.

### AIDE-STATE-002: Explicit Uncertainty

Not-run, skipped, blocked, failed, cancelled, inconclusive, stale, and
unknown-effect states MUST NOT be coerced to pass, complete, or zero.

### AIDE-STATE-003: Source-Bound Current Views

A current-status or next-action view MUST identify its source records, cutoff,
omissions, and stale inputs.

### AIDE-STATE-004: Revocable Qualification

Qualification and support claims MUST bind exact artifacts and environments and
state applicable expiry or revocation conditions.

### AIDE-STATE-005: No Count Inflation

Counts of files, tests, schemas, commits, tasks, or harvested records MUST NOT
alone establish capability completeness or release readiness.

### AIDE-STATE-006: Support Vocabulary

Maintenance posture MUST use support tiers `T0` through `T5`, and integration
depth MUST use capability levels `L0` through `L4`, without implying uniform
parity across hosts.

## Acceptance Direction

Acceptance should compare a schema-only feature with an operational prototype,
exercise a well-formed domain refusal from a successful process, preserve
unknown effect after timeout, expose a stale generated packet, revoke evidence
after subject bytes change, and reject count-only readiness claims.

These acceptance cases are desired tests, not qualification evidence.
