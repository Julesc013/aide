# WorkUnits, Attempts, and Decomposition

| Field | Value |
|---|---|
| Contract status | Adopted desired-state contract |
| Source family | S21 work and attempt contract, adapted to the live filesystem queue |
| Implementation | Partial across queue, attempt, evidence, and recovery records |
| Behavioral qualification | Not established by this document |
| Owner | Work coordinator within applicable policy and project authority |

## Principle

The unit of durable admitted intent is a WorkUnit. The unit of execution is an
attempt. The unit of side-effect uncertainty is an effect. These identities
must remain separate so retries, recovery, and review do not rewrite history.

A WorkUnit revision fixes its objective, scope, dependencies, budgets,
acceptance criteria, and stop conditions. Runtime state may advance without
changing that admitted revision. A retry creates a new immutable attempt and
retains the prior attempt's outputs, usage, failures, and unresolved effects.

This contract describes desired behavior. It does not migrate the current
filesystem queue, add fields to existing schemas, or authorize dispatch.

## Decomposition

Decomposition creates attributable child work and dependencies, not smaller
untracked prompts. Child work must preserve relevant parent constraints and
must rejoin through acceptance criteria that verify the complete parent result.
Passing isolated child checks does not establish that their combined output is
coherent.

WorkUnit size should follow risk and authority boundaries. Tiny state changes
do not each require a permanent task directory, while unrelated effects must
not be hidden inside one oversized unit. Concurrency, active-writer, and
completed-but-unintegrated limits belong to the admitted work profile.

Child permissions are intersections of inherited and explicitly delegated
limits. Model choice, reasoning effort, data access, billing, tool privileges,
and acceptance floors are independent controls; no model ranking can infer
effect authority.

## Requirements

### AIDE-WORK-001: Bounded Admitted Work

Non-trivial execution MUST bind a WorkUnit revision with a goal, non-goals,
source scope, dependencies, budgets, acceptance criteria, and stop conditions.

### AIDE-WORK-002: Immutable Attempts

Retries MUST create distinct immutable attempt identities while retaining prior
outputs, resource usage, failures, and uncertainty.

### AIDE-WORK-003: Intent Before Dispatch

Each consequential attempt or effect MUST persist its authorized intent before
the process, mutation, or remote request is launched.

### AIDE-WORK-004: Decomposition Coverage

Child work MUST preserve applicable parent constraints and MUST include
composition verification for the complete requested outcome.

### AIDE-WORK-005: Bounded Work In Progress

Scheduling MUST enforce declared concurrency, active-writer, and
completed-but-unintegrated limits for the applicable profile.

### AIDE-WORK-006: Scoped Continuation

Handoffs MUST identify the exact source state, retained candidate, evidence,
budget, unresolved effects, and next admissible actions.

### AIDE-WORK-007: Current Queue Preservation

Adopting this contract MUST NOT silently replace existing queue ownership,
task states, branch policy, or review gates.

## Acceptance Direction

Acceptance should cover protected free-form requests that lack admission,
traceable retries, failed intent persistence, disagreeing child outputs,
work-in-progress ceilings, restart from durable state, and advisory roadmaps
that conflict with queue truth.

These are desired acceptance cases. This document records none of them as run.
