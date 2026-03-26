# AIDE Planning Index

## Purpose

`PLANS.md` is the repository's working plan index for substantial engineering work. It exists to track real execution intent, dependencies, milestones, blockers, and verification plans. It is not a marketing roadmap.

## How Plans Are Structured

- Each substantial work item should have a stable identifier such as `P00`, `P01`, or a later program-specific id.
- A plan entry should describe one coherent objective.
- Plans should be updated as work progresses rather than rewritten after the fact.
- Status values should be explicit, for example `proposed`, `active`, `blocked`, `completed`, or `superseded`.

## Recommended Fields For A Plan Entry

- `Plan ID`
- `Title`
- `Status`
- `Objective`
- `Scope`
- `Allowed Paths`
- `Dependencies`
- `Milestones`
- `Blockers`
- `Verification Intent`
- `Exit Criteria`
- `Notes`

## Dependency Tracking

- Record upstream dependencies that must exist before the plan can finish.
- Record downstream work that depends on the plan when that relationship matters to execution order.
- Reference authoritative docs or prompts rather than relying on memory.

## Milestone Tracking

- Break work into small milestones with observable completion criteria.
- Use milestones to separate governance, scaffolding, implementation, verification, and packaging when those phases differ.
- Mark milestones complete only when the corresponding verification intent has been satisfied.

## Blocker Tracking

- Record blockers explicitly and name whether they are internal or external.
- Distinguish blocked work from intentionally deferred work.
- Remove or downgrade a blocker only when the blocking condition is actually resolved.

## Verification Intent

- State how the plan will be verified before the work is declared complete.
- Verification intent may include file checks, schema checks, tests, evals, or structural review depending on the task.
- If only structural verification is possible, say so up front.

## Entry Template

```md
### Plan ID: PX

- Title:
- Status:
- Objective:
- Scope:
- Allowed Paths:
- Dependencies:
- Milestones:
- Blockers:
- Verification Intent:
- Exit Criteria:
- Notes:
```

## Current Plan Index

### Plan ID: P00

- Title: AIDE repository constitution and operating law
- Status: Completed
- Objective: establish the root operating law, governance policies, and root planning and documentation templates
- Scope: `README.md`, root control-plane files, and `governance/` policy documents only
- Allowed Paths: `README.md`, `AGENTS.md`, `PLANS.md`, `IMPLEMENT.md`, `DOCUMENTATION.md`, `governance/vision.md`, `governance/support-policy.md`, `governance/naming-policy.md`, `governance/capability-levels.md`, `governance/release-policy.md`
- Dependencies: existing bootstrap control-plane commit `f2b4e72`
- Milestones: inspect current root docs; draft consistent governance set; verify conceptual anchors and required files; checkpoint a commit
- Blockers: none
- Verification Intent: file existence checks plus `rg` checks for required policy anchors and terminology
- Exit Criteria: all required files exist, the policy set is internally consistent, and verification passes
- Notes: governance only; no product implementation, inventory system, adapter code, packaging, CI, or environments in this prompt; conceptual-anchor verification passed

### Plan ID: P06

- Title: Shared-core architecture and host-adapter contract system
- Status: Completed
- Objective: define the canonical shared-core architecture, host-adapter contract, execution-mode model, and conservative shared schemas for later implementation prompts
- Scope: `specs/**`, `shared/**`, and root planning or documentation indexes only
- Allowed Paths: `PLANS.md`, `IMPLEMENT.md`, `DOCUMENTATION.md`, `specs/**`, `shared/**`
- Dependencies: P00 governance law, P01 inventory and matrices, P03 through P05 host-atlas research, and the existing host-lane scaffold under `hosts/**`
- Milestones: architecture narratives created under `specs/architecture/`; shared subtree scaffold created under `shared/`; machine-readable shared schemas created under `shared/schemas/`; root planning and documentation indexes updated to record the milestone
- Blockers: none
- Verification Intent: structural verification only, using file and directory existence checks, `rg` anchor checks for core contract terms and execution modes, and an allowed-path audit over the git diff
- Exit Criteria: architecture docs exist and are internally consistent, shared subtree directories and schema placeholders exist, planning or documentation indexes are updated, and verification passes
- Notes: architectural only; executable shared-core logic, host-adapter implementation, packaging, CI, environments, and eval wiring remain deferred
