# Authority and Decision Provenance

| Field | Value |
|---|---|
| Contract status | Adopted desired-state foundation |
| Source family | S21 authority contract, adapted to live AIDE policy |
| Implementation | Partial across queue, policy, and evidence surfaces |
| Behavioral qualification | Not established by this document |
| Owner | Policy and project owners within their scopes |

## Principle

Adopting specification text is a design decision. It is not permission to
execute, spend, mutate a target, integrate a branch, publish an artifact, or
weaken a target project's authority.

There is no useful single ranking for every kind of truth:

- reviewed product contracts define intended behavior;
- exact source and tests define implementation facts;
- observations and evidence define bounded qualification facts;
- current policy, actor identity, and grants define permission;
- release records define support and publication claims.

Generated status pages project these facts. They do not replace their owners.

## Provenance Classes

AIDE MUST keep these classes distinguishable:

1. Direct owner instruction.
2. Reviewed and adopted decision.
3. Proposal or recommendation.
4. Current implementation observation.
5. Test or operational observation.
6. Derived summary or generated projection.
7. Historical fact retained for attribution.

Quoting a proposal in a later prompt does not automatically turn it into an
adopted decision. A later decision supersedes only the scope it identifies.

## Requirements

### AIDE-AUTH-001: Separate Authority Axes

AIDE MUST represent intended behavior, observed behavior, permission, and
support as separate authority axes.

### AIDE-AUTH-002: No Self-Grant

A change MUST NOT gain approval solely by editing the policy, validator, test,
or specification used to judge that same change.

### AIDE-AUTH-003: Source-Bound Claims

A material decision or qualification claim MUST identify its subject, source,
cutoff, and evidence. Missing or summary-only inputs MUST remain visible.

### AIDE-AUTH-004: Distinct Effect Predicates

Permission to inspect, mutate, spend, integrate, close, tag, upload, or publish
MUST be represented as distinct predicates when those effects differ.

### AIDE-AUTH-005: Scoped Supersession

A superseding decision MUST identify the prior decision and affected scope.
Unaffected historical facts, failures, and obligations remain attributable.

### AIDE-AUTH-006: Target Ownership

Target repositories retain their domain, mutation, validation, and release
authority unless an explicit target-owned contract delegates a bounded part.

## Acceptance Direction

Acceptance should demonstrate that loading a newly adopted specification grants
no additional tool authority; stale README claims cannot override missing
qualification; quoted recommendations remain proposals; self-edited policy is
not its own oracle; and a successful process exit cannot substitute for an
observed integration result.

These acceptance cases are desired tests, not qualification evidence.
