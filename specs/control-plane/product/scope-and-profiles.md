# Product Scope and Profiles

| Field | Value |
|---|---|
| Contract status | Adopted desired-state foundation |
| Source family | S21 product scope, adapted to live AIDE terminology |
| Implementation | Partial and profile-specific |
| Behavioral qualification | Not established by this document |
| Owner | Product contract |

## Purpose

AIDE is a repo-native development control plane for preserving work, expressing
authority, compiling reproducible context, coordinating bounded execution, and
retaining evidence. Its product value is the quality and continuity of those
workflows, not the number of schemas, reports, prompts, or generated files.

## Product Boundary

AIDE coordinates humans, deterministic tools, coding agents, host adapters,
tests, and authoring surfaces. It does not absorb a target project's product
law, become the sole authority that approves its own changes, or require every
target executable to embed an AIDE runtime.

The AIDE source repository is one self-hosting consumer. It is not a universal
project template, and its generated queue or evidence volume is not itself a
measure of product capability.

## Compositions

Product surfaces are compositions over shared contracts:

- **Lite** provides portable local adoption, inspection, planning, validation,
  context, and evidence capabilities.
- **CLI** exposes command-oriented workflows.
- **TUI** may present CLI use cases without creating a second task authority.
- **Service** may provide optional durable coordination.
- **Workbench** may provide a richer operator experience.
- **Commander** may supervise multiple repositories without replacing each
  repository's task and product authority.

Independent packaging is justified only by deployment, lifecycle, or support
needs. It must not create divergent identities or cloned cores.

## Baseline Profile

The first stable profile is intentionally bounded. It should provide:

1. Brownfield repository observation before mutation.
2. Explicit ownership and authority boundaries.
3. Bounded planning and restartable WorkUnits.
4. Reusable validation, context compilation, and evidence.
5. Supported install, repair, update, rollback, and removal behavior.
6. Honest offline and unavailable-capability behavior.

Continuous workers, fleet operation, every host integration, advanced domain
authoring, and unattended integration may exist as optional or incubating
profiles. A smaller profile's qualification does not certify them.

## Requirements

### AIDE-SCOPE-001: Durable Work

AIDE MUST keep durable work, decisions, and evidence independent of a particular
model conversation, editor window, provider, or execution-host session.

### AIDE-SCOPE-002: No-Model Value

The baseline profile MUST provide useful local inspection, planning, validation,
and knowledge navigation without inference or network access.

### AIDE-SCOPE-003: Target Authority

AIDE MUST preserve target ownership of domain meaning, canonical validation,
mutation, and release decisions.

### AIDE-SCOPE-004: Bounded Qualification

Release and support claims MUST name the exact capability profile, artifact,
environment, and evidence. They MUST NOT infer whole-product readiness from a
smaller accepted profile.

### AIDE-SCOPE-005: Shared Identities

CLI, TUI, Service, Workbench, and Commander MUST resolve shared work and object
identities rather than creating independent task copies.

### AIDE-SCOPE-006: Consumer Before Expansion

A proposed public contract MUST identify a producer, consumer, user journey,
and executable acceptance path before implementation admission.

### AIDE-SCOPE-007: Replaceable Integrations

External execution hosts, graph services, vector stores, cloud runtimes, model
providers, and package registries MUST remain replaceable bounded bindings.

## Acceptance Direction

Acceptance must exercise a pinned profile and observable user loop. At minimum,
tests should cover provider removal after completion, all-provider-disabled
operation, target-policy conflict, narrow-profile qualification, shared identity
across surfaces, contract proposals without consumers, and optional integration
removal.

These acceptance cases are desired tests. They are not recorded as run by this
document.
